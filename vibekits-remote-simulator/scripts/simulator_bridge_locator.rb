# Locate a live process-owned controller bridge, without copying credentials.
require 'json'
require 'uri'
require 'socket'
require 'open3'

module SimulatorBridgeLocator
  def self.live(path, app_pids)
    return nil unless File.file?(path)
    stat = File.stat(path)
    return nil unless stat.uid == Process.uid && (stat.mode & 0o077).zero?
    value = JSON.parse(File.read(path))
    pid = value['processId']
    return nil unless pid.is_a?(Integer) && app_pids.include?(pid)
    uri = URI.parse(value.fetch('endpoint'))
    return nil unless uri.scheme == 'http' && %w[127.0.0.1 ::1 localhost].include?(uri.host)
    return nil if value['token'].to_s.empty?
    Socket.tcp(uri.host, uri.port, connect_timeout: 1) { |socket| socket.close }
    [path, value]
  rescue JSON::ParserError, KeyError, URI::InvalidURIError, SystemCallError, IOError
    nil
  end

  def self.locate(default_path)
    output, status = Open3.capture2('ps', '-axo', 'pid=,comm=')
    raise 'CONTROL_BRIDGE_PROCESS_CHECK_FAILED' unless status.success?
    app_pids = output.lines.map do |line|
      match = line.match(/^\s*(\d+)\s+(.+)$/)
      match[1].to_i if match && match[2].strip.end_with?('/Contents/MacOS/Vibekits')
    end.compact
    explicit = ENV['VIBEKITS_TOOL_BRIDGE_FILE'].to_s.strip
    unless explicit.empty?
      result = live(explicit, app_pids)
      raise 'CONTROL_BRIDGE_EXPLICIT_PATH_NOT_LIVE' unless result
      return result
    end
    result = live(default_path, app_pids)
    return result if result
    candidates = app_pids.flat_map do |pid|
      # Capture privately; never print environment, token or config contents.
      env, ok = Open3.capture2('ps', 'eww', '-p', pid.to_s)
      next [] unless ok.success?
      match = env.match(/(?:^| )VIBEKITS_DATA_HOME=(.*?)(?= [A-Za-z_][A-Za-z0-9_]*=|\n|\z)/m)
      next [] unless match && match[1].start_with?('/')
      %w[Mcp mcp].map { |dir| File.join(match[1], dir, 'tool-bridge.json') }
    end
    results = candidates.uniq.map { |path| live(path, app_pids) }.compact
    # APFS often treats Mcp/mcp as the same file; count the inode once.
    results = results.uniq { |path, _| stat = File.stat(path); [stat.dev, stat.ino] }
    raise 'CONTROL_BRIDGE_UNAVAILABLE: no live controller bridge; remote device state unknown' if results.empty?
    raise 'CONTROL_BRIDGE_AMBIGUOUS: select a verified VIBEKITS_TOOL_BRIDGE_FILE' if results.length > 1
    results.first
  end
end
