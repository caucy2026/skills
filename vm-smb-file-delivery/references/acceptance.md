# Evidence and acceptance matrix

Record the following without secrets.

| Layer | Minimum evidence | What it does not prove |
|---|---|---|
| VM identity | VM name/config path, guest OS, IP, timestamp | guest services are healthy |
| Transport | TCP 445 connection or verified native transport | authentication or file access |
| Authentication | successful login and share enumeration | destination is writable |
| Delivery | remote path plus uploaded byte count | remote bytes match |
| Integrity | SMB read-back with byte/digest equality | payload executed |
| Mapping | `net use` and `dir X:\` in intended user session | two-way synchronization |
| Host to guest | unique host test file visible with matching content in guest | guest to host works |
| Guest to host | unique guest test file visible with matching content on host | persistence works |
| Persistence | re-login/restart observation with mapping restored | business payload works |
| Execution | explicit process/output/readiness evidence | application behavior is correct |

## Recommended report

Include:

- exact requested outcome;
- selected transport and why;
- preflight observations;
- source and destination identities;
- overwrite/backup decision;
- read-back size and digest;
- mapped-drive session identity, if applicable;
- host-to-guest and guest-to-host results, if applicable;
- actions deliberately not taken;
- rollback location or procedure;
- remaining unverified layers.

Use status labels such as `PASS`, `FAIL`, `NOT RUN`, and `BLOCKED`, not ambiguous prose. A manual desktop click can remain `NOT RUN` while direct SMB delivery is `PASS`.

## Cleanup

Remove only experiment-owned temporary files after confirming they are not the delivered payload or rollback copy. Never delete backups, VM images, guest files, mappings, or synchronization roots merely because an experiment ended.
