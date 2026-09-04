---
name: vibekits-remote-node
description: Discover, inspect, connect to, diagnose, and operate VibeKits remote simulation, build, MCP, desktop, or Android nodes across Windows, macOS, Linux, and Android. Use for cross-device builds, LAN MCP coordination, SSH access, RustDesk/ADB simulation, registered node recovery, or platform validation; do not use for unrelated remote hosts.
---

# VibeKits Cross-Platform Remote Nodes

Use this skill as the durable cross-platform contract for VibeKits remote simulation and agent-operated nodes.

## Route the task

1. Read [references/common-contract.md](references/common-contract.md) for every task involving discovery, identity, authentication, authorization, tool selection, long-running work, or evidence.
2. Detect the target operating system and transport before composing commands. Then read only the relevant section of [references/platform-adapters.md](references/platform-adapters.md).
3. When the target is the registered Windows node at `192.168.3.58`, also read [references/windows-58.md](references/windows-58.md).
4. The relevant specifications are bundled under `references/specs`; read [references/specs/INDEX.md](references/specs/INDEX.md) for provenance and safety boundaries. No author-local checkout is needed to load this skill. Building an application still requires its source and platform toolchain. Detect and report protocol/implementation drift rather than silently accepting incompatible behavior.

## Preserve these invariants

- Never assume the controller and target use the same OS, shell, path syntax, CPU architecture, privilege model, or packaging format.
- Keep project, dependency, cache, temporary, build, log, and test data off the operating-system volume when the user or node contract requires it. The Windows `D:` rule applies to registered Windows build nodes; use a configured non-system data/work volume on macOS/Linux rather than inventing a `D:` path.
- Verify host, peer, device, or LMCP instance identity before authentication or tool execution. Never disable SSH host checking, TLS pinning, caller signing, or equivalent identity validation to force success.
- Use advertised MCP schemas dynamically. Do not guess tool names or parameters from an earlier catalog revision.
- Local Harness tool use follows the app's granted operating scope. A remote caller must satisfy the provider's persisted pairing/authorization scope. Do not add per-call prompts where an existing valid scope authorizes unattended execution.
- Never store or print private keys, passwords, access tokens, instance private certificates, RustDesk session credentials, or other secrets.
- Diagnose read-only first. Mutating accounts, ACLs, services, firewall, pairing, installs, devices, files, or running processes requires authority for that task.
- Long-running and repeated tasks need a task ID, progress/status path, cancellation behavior, health checks, bounded retries, abort conditions, and resumable evidence.

## Completion standard

Report the requested outcome rather than transport success. State which stages passed, failed, or were blocked: discovery, identity, authorization, capability refresh, source sync, build, artifact integrity, deployment, launch, functional validation, compatibility, performance, stress/repetition, upgrade/rollback, and cleanup. Include the first causal failure and concrete next prerequisite.
