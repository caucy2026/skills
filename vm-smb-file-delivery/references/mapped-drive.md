# Host folder synchronization and Windows mapped drives

Use this mode when a host folder must be accessible through a Windows drive letter such as `Z:`.

## Discover the actual architecture

Do not infer a working share from the VM configuration UI. Establish which architecture is truly present:

1. **Native guest transport:** SPICE WebDAV, VirtioFS, VMware shared folders, Parallels tools, or another guest agent exposes the host directory directly.
2. **Guest-local SMB bridge:** Windows shares a local directory such as `C:\PublicShare`; a host-side process synchronizes that directory over SMB; the interactive Windows user maps `Z:` to `\\127.0.0.1\PublicShare` or the guest hostname.
3. **Host SMB server:** Windows maps a drive directly to a host SMB share. This can be unsuitable for old guests when dialect and authentication support do not overlap.

Record the selected architecture, authoritative folder, synchronization direction, conflict policy, deletion policy, and expected latency. Never combine paths from two architectures under the same friendly name.

## Safe restoration order

1. Inspect the current mapping with `net use` before deleting or replacing it.
2. Confirm the underlying target is reachable and readable using a temporary drive letter or direct UNC path.
3. Preserve an existing working mapping if the candidate target fails.
4. Create the final mapping in the intended interactive user's session.
5. Use `/persistent:yes` only when persistent reconnection is requested.
6. Verify the mapping from that same desktop session.

Example for a verified guest-local share:

```bat
net use
dir \\127.0.0.1\PublicShare
net use Z: \\127.0.0.1\PublicShare /persistent:yes
dir Z:\
```

Deleting an existing `Z:` mapping is destructive to that session. Do it only after the replacement endpoint is proven or after explicit user authorization.

## Synchronizer rules

For a host-driven two-way synchronization bridge:

- run a single instance with auditable logs and bounded retry/backoff;
- never store credentials in the synchronizer source or command line;
- default to no deletion propagation;
- preserve conflict copies rather than silently selecting a winner;
- compare content, not only timestamps, when clocks may differ;
- ignore temporary, lock, and partial-upload files by an explicit policy;
- stage and rename when consumers may read files concurrently;
- stop synchronization before changing the authoritative-root definition.

One manual synchronization pass does not prove real-time or continuous sharing. Claim continuous operation only after the background process, restart behavior, latency, and conflict handling have been observed.

## Native shared-folder caution

A configured WebDAV/shared-directory mode is only intent. Verify the guest agent/service, listener or redirector, test drive, and actual file visibility. If the expected endpoint is absent, record that transport as unavailable and fall back to an already proven SMB route; do not install unknown guest components or replace a working mapping without authorization.
