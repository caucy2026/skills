# Direct SMB delivery to a running Windows guest

Use this mode for a one-time or batch upload to an authorized Windows VM without manipulating its virtual disk or desktop GUI.

## Preflight

Resolve rather than guess:

- guest IP and TCP 445 reachability;
- Windows `LanmanServer`/Server service state;
- available shares (`net share` in the guest or authenticated enumeration);
- exact remote directory and whether the profile uses `Desktop`, a localized name, or another deployment folder;
- share permissions and NTFS permissions;
- architecture and encoding constraints for the payload.

ICMP failure does not prove SMB failure. Treat a successful TCP 445 connection as transport evidence only; authentication and write access still require separate checks.

For legacy guests such as Windows XP or Server 2003, use a client library that supports the guest's negotiated SMB dialect. Do not respond to a compatibility failure by exposing an unauthenticated share or globally weakening the host.

## Transfer transaction

1. Create a unique local staging directory containing only the intended payload.
2. Compute local size and a strong digest when tooling permits.
3. Authenticate using runtime-only credentials.
4. Enumerate or probe the destination directory before writing.
5. If the destination exists, download it first and preserve a timestamped backup unless overwrite policy is already established.
6. Upload to a temporary remote name when atomic replacement is needed, verify it, then rename within the same share.
7. Download the resulting remote file through SMB.
8. Compare bytes, size, and digest with the local source.
9. Log only nonsensitive identities: host alias/IP, share, destination, size, digest, timestamp, and result.

An `uploaded` return value is not the acceptance gate. Read-back equality is.

## Useful guest-side checks

On older Windows guests, these commands are useful read-only evidence:

```bat
sc query LanmanServer
net share
netstat -an | find ":445"
dir "C:\path\to\destination"
```

## Failure routing

| Symptom | Evidence boundary | Next safe check |
|---|---|---|
| Connection refused | SMB listener unavailable | Server service, firewall, exact IP |
| Timeout | route or guest availability unknown | virtual NIC/host route, then retry TCP 445 |
| Logon failure | credentials rejected | re-enter securely; do not change sharing policy |
| Access denied | share or NTFS authorization failed | intended account and destination permissions |
| Bad network name | share does not exist | authenticated share enumeration or guest `net share` |
| Object path not found | destination path is wrong | list parent paths before writing |
| Upload reports success but content differs | stale/partial/translated file | download, byte-compare, preserve both versions |

Do not execute the transferred file unless the user separately requested execution and the target/process impact has been checked.
