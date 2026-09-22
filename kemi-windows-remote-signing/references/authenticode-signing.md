# Windows Authenticode signing

Use this procedure for KEMI Windows desktop releases when a code-signing certificate is available through iTrus, SafeNet, a Windows certificate store, or a hardware token.

## Choose the signing path

`iTrusSignTool` is a GUI wrapper around Windows Authenticode. Its documented automation path is Microsoft `signtool.exe`; do not invent undocumented iTrus command-line switches.

1. Stage the maintained helper at an explicit `D:\KEMI-Test\work\...` path and run `Inspect` in the same Windows account and session that will sign:

   ```powershell
   pwsh -NoProfile -File D:\KEMI-Test\work\Invoke-KemiAuthenticode.ps1 -Mode Inspect
   ```

2. Record the x64 SignTool path/version and select exactly one unexpired certificate that has a private key and Code Signing EKU (`1.3.6.1.5.5.7.3.3`). Pass its current SHA-1 thumbprint explicitly. Historical release thumbprints are evidence only; never reuse one without re-enumerating the current store.
3. Treat SSH Session 0 and the interactive desktop account as separate security contexts. `Inspect` returning no usable certificate in SSH does **not** prove that the certificate is missing. If `Sign` reports `INTERACTIVE_SIGNING_REQUIRED`, use the project's allowlisted interactive agent or run the same fixed script in the already logged-in, unlocked desktop account. Do not create an arbitrary scheduled task, export a non-exportable EV key, or weaken token policy.
4. Prefer one SignTool invocation for a batch so a hardware token asks for its PIN only once. A second signing phase may require another PIN because the token middleware does not have to cache authentication across processes.

## Interactive launch checkpoint

Treat a previously successful interactive wrapper as a release record. Preserve it under its descriptive or versioned name; never overwrite it with a newly generated wrapper. Before reuse, read the wrapper and confirm the exact input path, expected file count, current certificate thumbprint, description, and report path. If any field is stale, create a new versioned wrapper beside it and leave the known-good entry unchanged.

On a KEMI/RustDesk desktop session, use the same Explorer launch route that was proven for that node: open the fixed `D:\KEMI-Test\work` directory, search for the exact wrapper filename, single-select the exact result, verify its full path and previewed command, and invoke Explorer's **Open** action. When similar filenames appear, never rely on row position, a pre-existing highlight, a double-click, or the Enter key alone; these can select the wrong result or open the script in an editor through the remote session.

Within 10 seconds of invoking the wrapper, require one of these observable signals: the SafeNet/iTrus PIN prompt, a live `signtool`/helper process in the interactive session, or a freshly updated signing report. If none appears, classify the attempt as `INTERACTIVE_WRAPPER_NOT_STARTED`; stop clicking, reselect the exact result, and correct the launch action. Do not call this a certificate or signing failure, and do not retry SignTool from SSH. After the PIN is entered, require the wrapper exit code and the fresh report before considering signing complete.

## Deterministic command contract

Do not use `/a` for a release: it silently delegates signer selection and can choose a different certificate when the store changes. Use the maintained helper with the exact expected thumbprint, explicit input list, optional expected count, and a report path on `D:`:

```powershell
$inner = Get-ChildItem -LiteralPath 'D:\KEMI-Test\app\product-staged' -Recurse -File |
  Where-Object Extension -in '.exe', '.dll' |
  Sort-Object FullName

pwsh -NoProfile -File D:\KEMI-Test\work\Invoke-KemiAuthenticode.ps1 `
  -Mode Sign `
  -Path $inner.FullName `
  -ExpectedFileCount $inner.Count `
  -ExpectedThumbprint 'CURRENT_CERTIFICATE_THUMBPRINT' `
  -Description 'KEMI Product Name' `
  -ReportPath 'D:\KEMI-Test\results\signing\inner-sign.json'
```

The helper fails closed when the session, D-drive boundary, certificate, private key, EKU, expiry, input count, signer thumbprint, timestamp, Authenticode status, or SignTool verification is wrong. A PIN stays in the token middleware prompt; it is never a script parameter.

After the project-specific packer rebuilds the outer package from the signed staged directory, invoke the helper a second time for the single outer file. Never let a generic signing helper guess or execute the product's pack command.

## Failure routing

| Evidence | Meaning | Required action |
|---|---|---|
| `INTERACTIVE_SIGNING_REQUIRED` | Signing was attempted from Session 0 | Run the same script through the approved interactive path; do not retry SSH |
| `CERTIFICATE_NOT_FOUND` in SSH only | Current SSH account/store cannot see the certificate | Inspect in the logged-in signer account before concluding the certificate is absent |
| `PRIVATE_KEY_UNAVAILABLE` | Certificate metadata is visible but its private key is not usable | Check token insertion, middleware, signer account, and desktop session; never export/replace the key as a shortcut |
| `CERTIFICATE_EXPIRED` or wrong EKU | The selected certificate is unusable | Stop release and obtain the correct current certificate |
| SignTool cancellation/PIN error | Human/token authentication did not complete | Preserve log and retry once from the same interactive session; do not embed the PIN |
| `SIGNER_MISMATCH`, missing timestamp, or verify failure | Output does not meet release identity/integrity gates | Quarantine the artifact and do not package/publish it |

## Final installer and portable-package order

For every distributable Windows `.exe`, including Inno Setup installers and self-extracting portable packages, the byte order is mandatory:

1. Freeze the Release directory and inventory every `.exe` and `.dll` with size and SHA-256.
2. Sign all inner PE files in one SignTool invocation.
3. Verify every inner signature before packaging. Reject any missing file, unexpected file-count change, invalid signature, wrong signer, or missing timestamp.
4. Build the final outer installer or portable executable from the signed staged files. Record its exact output path; do not substitute an older, similarly named installer.
5. Sign that final outer `.exe` after the packer finishes. A signed embedded application does not make an unsigned Inno Setup or portable wrapper signed. Signing inner files after packaging does not update the bytes already embedded in the outer package.
6. Run `Get-AuthenticodeSignature` and `signtool verify /pa /all /v` on the **exact final outer `.exe` that will be uploaded**. Require `Valid`, the intended signer, a trusted timestamp, and a successful SignTool exit code. Fail the release if the wrapper is unsigned or verification fails, even when every embedded PE is signed.
7. Recompute the final package size and SHA-256 after the outer signature; signing changes the file hash. Match that size and SHA-256 to the upload candidate and, where the platform exposes it, to the received submission. Any repackaging or modification requires repeating outer signing and verification.

Use SHA-256 file digests and an RFC 3161 SHA-256 timestamp unless the project or certificate issuer requires another supported policy. The helper's invocation shape is intentionally deterministic:

```powershell
$arguments = @(
  'sign', '/v', '/s', 'My', '/sha1', $expectedThumbprint,
  '/fd', 'SHA256',
  '/tr', 'http://timestamp.digicert.com',
  '/td', 'SHA256',
  '/d', 'KEMI Remote Office'
)
$arguments += $files.FullName
& $signTool @arguments
if ($LASTEXITCODE -ne 0) { throw "SignTool failed: $LASTEXITCODE" }
```

Pass the full batch as an argument array rather than constructing a shell string. Do not put a PFX password or hardware-token PIN in a command, script, environment variable, log, or release report.

The repository's legacy `client/build.py` PFX/password branch (`P`, `cert.pfx`, `/p`, `/t`) is not the KEMI release signing path: it exposes a password through process construction, uses legacy timestamp syntax, signs only one pre-package file, and cannot prove the final outer package. Do not set `P` or copy a PFX into a worktree. Build unsigned staged bytes first, then use the maintained two-phase flow above.

PowerShell 5 can turn a native program's normal stderr progress into `NativeCommandError` when `$ErrorActionPreference = 'Stop'`. When a build or packer writes normal progress to stderr, run that native command through `cmd.exe` with explicit log redirection and check its exit code; do not disable error handling for the rest of the release script.

## Verification evidence

For every inner PE and the final outer package, collect:

- `Get-AuthenticodeSignature` status, signer subject, signer thumbprint, and timestamp certificate;
- `signtool verify /pa /all /v` exit code and output;
- exact bytes and SHA-256 after the final signature;
- source commit and product version.

Then run the packaged application in the interactive desktop account and perform the project's launch, close, relaunch, upgrade, market install/open, connection, disconnect, and input regression checks. A valid Authenticode result alone is not installation acceptance.

## Known-good evidence, not configuration

KEMI Remote Office `1.4.125+241` was successfully signed on Windows test node 58 in the interactive desktop context: 15 inner PE files were signed before packaging, the outer portable EXE was signed last, Windows reported `Valid`, and `signtool verify /pa /all /v` reported one passed outer signature with a DigiCert RFC 3161 timestamp. Its recorded certificate thumbprint must remain historical evidence; every new release must discover and select the current valid certificate again.
