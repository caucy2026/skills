#!/usr/bin/env python3
"""Read a bounded Windows evidence file over the authorized simulator SSH.

Fallback when screenshot capture succeeds but SFTP closes. This is read-only;
call simulator.connect and verify the target identity before invoking it.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess


def read_file(routing_id, remote_path, output):
    if not re.fullmatch(r'\d{6,16}', routing_id):
        raise ValueError('invalid simulator ID')
    if not re.match(r'^[A-Za-z]:\\', remote_path) or any(
        c in remote_path for c in '\r\n\0'
    ):
        raise ValueError('expected Windows absolute file path')
    quoted = "'" + remote_path.replace("'", "''") + "'"
    invoke = Path.home() / '.codex/skills/vibekits-remote-simulator/scripts/invoke.rb'

    def ssh(script):
        script = '[Console]::OutputEncoding=[Text.UTF8Encoding]::new();' + script
        encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
        args = {'routingId': routing_id, 'command':
                'powershell.exe -NoProfile -NonInteractive -EncodedCommand ' + encoded}
        result = subprocess.run(
            ['ruby', str(invoke), 'vibekits.simulator.ssh_exec', json.dumps(args)],
            capture_output=True, text=True, timeout=45, check=True,
        )
        value = json.loads(result.stdout)
        data = value.get('data', {})
        if value.get('ok') is not True or data.get('exitCode') != 0:
            raise RuntimeError('simulator read failed; inspect target state')
        return data['stdout'].strip()

    facts = json.loads(ssh(
        '$p=' + quoted + ';$f=Get-Item -LiteralPath $p;'
        '@{length=$f.Length;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash}'
        '|ConvertTo-Json -Compress'
    ))
    size = facts['length']
    if not isinstance(size, int) or not 0 < size <= 8 * 1024 * 1024:
        raise ValueError('evidence file outside 1 byte–8 MiB bound')
    contents = bytearray()
    for offset in range(0, size, 16000):
        reply = ssh(
            '$f=[IO.File]::OpenRead(' + quoted + ');$f.Position=' + str(offset) + ';'
            '$b=New-Object byte[] 16000;try{$n=$f.Read($b,0,16000)}finally{$f.Dispose()};'
            '[Convert]::ToBase64String($b,0,$n)'
        )
        chunk = base64.b64decode(reply, validate=True)
        if len(chunk) != min(16000, size - offset):
            raise RuntimeError('short evidence chunk')
        contents.extend(chunk)
    digest = hashlib.sha256(contents).hexdigest()
    if digest != facts['sha256'].lower():
        raise RuntimeError('evidence hash changed during read')
    target = Path(output)
    if target.exists():
        raise FileExistsError('choose a fresh evidence filename')
    target.write_bytes(contents)
    return {'routingId': routing_id, 'path': str(target.resolve()),
            'bytes': size, 'sha256': digest}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True)
    parser.add_argument('--remote-path', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(read_file(args.id, args.remote_path, args.output)))
