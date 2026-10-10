# VibeKits remote-simulation tool contract

Inside VibeKits Harness, call registered MCP tools directly. Use `vibekits.simulator.catalog` if a tool schema is not yet known. Never reveal local bridge credentials.

## Controller tools

- `vibekits.simulator.connect`: `routingId`.
- `vibekits.simulator.connection_status`: `routingId`.
- `vibekits.simulator.catalog`: `routingId`.
- `vibekits.simulator.call`: `routingId`, `toolId`, `arguments`.
- `vibekits.simulator.ssh_exec`: `routingId`, one exact `command`.
- `vibekits.simulator.upload_file`: `routingId`, `localPath`.
- `vibekits.simulator.download_file`: `routingId`, `remotePath`.
- `vibekits.simulator.screenshot`: `routingId`.
- `vibekits.simulator.disconnect`: `routingId`.

## Remote device tools

Call through `vibekits.simulator.call` with the current catalog schema:

- `vibekits.device.processes`: running state/resource use.
- `vibekits.device.applications`: installed identity/version/path.
- `vibekits.device.logs` and `vibekits.device.crash_reports`: bounded diagnostics.
- `vibekits.device.ui_inspect` and `vibekits.device.screenshot`: permitted visual/AX evidence.
- `vibekits.device.ui_action`: only for requested, non-destructive interaction or with explicit authority for consequential actions.
- `vibekits.device.app_control`, `vibekits.device.app_install`, `vibekits.device.app_uninstall`: only when in task scope.

Examples for an external macOS controller without the registered MCP tools, from this skill folder:

```bash
ruby scripts/invoke.rb vibekits.simulator.connect '{"routingId":"123456789"}'
ruby scripts/invoke.rb vibekits.simulator.call '{"routingId":"123456789","toolId":"vibekits.device.applications","arguments":{"limit":50}}'
ruby scripts/invoke.rb vibekits.simulator.disconnect '{"routingId":"123456789"}'
```

The loopback bridge can wrap tool results in `content` and `structuredContent`. Check nested `ok`, `connected`, identity, authorization and tool-result fields; HTTP success alone is insufficient. Redact secrets and cap output.

## Windows覆盖升级的实际观察错误

复用[619控制器排障记录](https://github.com/caucy2026/vibekits/blob/main/docs/acceptance/WINDOWS619_UPGRADE_CONTROLLER_LESSONS_20261011.md)：脚本解析不证明函数作用域；活跃资源日志用允许写共享的有界读取，读取错误不能写成零样本；计划任务Ready要结合结果、PID/出生和回执。系统应用控制阻止诊断EXE时不包装重跑它或更改策略；允许的系统计数接口可独立采集同一资源指标。只对只读busy有界重读，未知安装/签名仍只对账原事务。以实际采样起止和缺项判定，不用帧数冒称五分钟或长期稳定。
