[CmdletBinding()]
param(
    [ValidateSet('Inspect', 'Sign', 'Verify')]
    [string]$Mode = 'Inspect',

    [string[]]$Path = @(),
    [string]$ExpectedThumbprint = '',
    [string]$Description = 'KEMI Windows Application',
    [string]$SignToolPath = '',
    [int]$ExpectedFileCount = 0,
    [string]$ReportPath = '',
    [switch]$AllowSessionZeroSoftwareKey
)

$ErrorActionPreference = 'Stop'
$codeSigningEku = '1.3.6.1.5.5.7.3.3'
$timestampUrl = 'http://timestamp.digicert.com'

function Normalize-Thumbprint([string]$Value) {
    return ($Value -replace '[^0-9A-Fa-f]', '').ToUpperInvariant()
}

function Get-EkuValues($Certificate) {
    return @($Certificate.EnhancedKeyUsageList | ForEach-Object {
        if ($_.ObjectId -is [System.Security.Cryptography.Oid]) {
            $_.ObjectId.Value
        } else {
            [string]$_.ObjectId
        }
    })
}

function Resolve-SignTool([string]$RequestedPath) {
    if ($RequestedPath) {
        $resolved = (Resolve-Path -LiteralPath $RequestedPath).Path
        if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) {
            throw "SIGNTOOL_NOT_FOUND: $RequestedPath"
        }
        return $resolved
    }

    $kitsRoot = Join-Path ${env:ProgramFiles(x86)} 'Windows Kits\10\bin'
    $candidate = Get-ChildItem -LiteralPath $kitsRoot -Recurse -File -Filter 'signtool.exe' -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '\\x64\\signtool\.exe$' } |
        Sort-Object { try { [version]$_.Directory.Parent.Name } catch { [version]'0.0' } } -Descending |
        Select-Object -First 1
    if (-not $candidate) { throw 'SIGNTOOL_NOT_FOUND: install a Windows SDK x64 SignTool.' }
    return $candidate.FullName
}

function Get-CodeSigningCertificates {
    return @(Get-ChildItem Cert:\CurrentUser\My | Where-Object {
        $ekuValues = Get-EkuValues $_
        $_.HasPrivateKey -and ($ekuValues -contains $codeSigningEku)
    } | Sort-Object NotAfter -Descending)
}

function Resolve-InputFiles([string[]]$RequestedPaths) {
    $files = @($RequestedPaths | ForEach-Object {
        $resolved = (Resolve-Path -LiteralPath $_).Path
        $item = Get-Item -LiteralPath $resolved
        if ($item.PSIsContainer) { throw "INPUT_NOT_FILE: $resolved" }
        if ($item.Extension -notin '.exe', '.dll', '.msi', '.msix') {
            throw "UNSUPPORTED_SIGNING_INPUT: $resolved"
        }
        if ($resolved -notmatch '^[Dd]:\\KEMI-Test\\') {
            throw "D_DRIVE_BOUNDARY_VIOLATION: $resolved"
        }
        $item
    } | Sort-Object FullName -Unique)

    if ($files.Count -eq 0) { throw 'NO_INPUT_FILES' }
    if ($ExpectedFileCount -gt 0 -and $files.Count -ne $ExpectedFileCount) {
        throw "INPUT_COUNT_MISMATCH: expected $ExpectedFileCount, found $($files.Count)"
    }
    return $files
}

function Resolve-Certificate([string]$Thumbprint) {
    $normalized = Normalize-Thumbprint $Thumbprint
    if (-not $normalized) { throw 'EXPECTED_THUMBPRINT_REQUIRED' }
    $certificate = Get-ChildItem Cert:\CurrentUser\My | Where-Object {
        (Normalize-Thumbprint $_.Thumbprint) -eq $normalized
    } | Select-Object -First 1
    if (-not $certificate) { throw "CERTIFICATE_NOT_FOUND: $normalized" }
    if (-not $certificate.HasPrivateKey) { throw "PRIVATE_KEY_UNAVAILABLE: $normalized" }
    if ($certificate.NotAfter -le (Get-Date)) { throw "CERTIFICATE_EXPIRED: $($certificate.NotAfter.ToString('o'))" }
    $ekuValues = Get-EkuValues $certificate
    if ($ekuValues -notcontains $codeSigningEku) { throw "CODE_SIGNING_EKU_MISSING: $normalized" }
    return $certificate
}

function Invoke-Native([string]$Executable, [string[]]$Arguments) {
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $output = @(& $Executable @Arguments 2>&1 | ForEach-Object { $_.ToString() })
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousPreference
    }
    return [pscustomobject]@{ ExitCode = $exitCode; Output = $output }
}

function Test-SignedFile($File, [string]$Thumbprint, [string]$ToolPath) {
    $signature = Get-AuthenticodeSignature -LiteralPath $File.FullName
    $actualThumbprint = if ($signature.SignerCertificate) {
        Normalize-Thumbprint $signature.SignerCertificate.Thumbprint
    } else { '' }
    $verify = Invoke-Native $ToolPath @('verify', '/pa', '/all', '/v', $File.FullName)
    $timestampSubject = if ($signature.TimeStamperCertificate) {
        $signature.TimeStamperCertificate.Subject
    } else { '' }
    $valid = ($signature.Status -eq 'Valid') -and
        ($actualThumbprint -eq $Thumbprint) -and
        [bool]$timestampSubject -and
        ($verify.ExitCode -eq 0)
    return [pscustomobject]@{
        Path = $File.FullName
        Bytes = $File.Length
        Sha256 = (Get-FileHash -LiteralPath $File.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        Status = [string]$signature.Status
        SignerSubject = if ($signature.SignerCertificate) { $signature.SignerCertificate.Subject } else { '' }
        SignerThumbprint = $actualThumbprint
        TimestampSubject = $timestampSubject
        SignToolVerifyExitCode = $verify.ExitCode
        Valid = $valid
    }
}

$sessionId = [System.Diagnostics.Process]::GetCurrentProcess().SessionId
$tool = Resolve-SignTool $SignToolPath

if ($Mode -eq 'Inspect') {
    $certificates = @(Get-CodeSigningCertificates | ForEach-Object {
        [pscustomobject]@{
            Subject = $_.Subject
            Thumbprint = Normalize-Thumbprint $_.Thumbprint
            NotBefore = $_.NotBefore.ToString('o')
            NotAfter = $_.NotAfter.ToString('o')
            HasPrivateKey = $_.HasPrivateKey
        }
    })
    [pscustomobject]@{
        Mode = $Mode
        User = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        SessionId = $sessionId
        InteractiveSigningExpected = ($sessionId -ne 0)
        SignToolPath = $tool
        SignToolVersion = (Get-Item -LiteralPath $tool).VersionInfo.FileVersion
        CodeSigningCertificates = $certificates
    } | ConvertTo-Json -Depth 5
    exit 0
}

if ($Mode -eq 'Sign' -and $sessionId -eq 0 -and -not $AllowSessionZeroSoftwareKey) {
    throw 'INTERACTIVE_SIGNING_REQUIRED: Session 0 cannot be assumed to have access to the hardware token or its PIN prompt.'
}

$files = Resolve-InputFiles $Path
$thumbprint = Normalize-Thumbprint $ExpectedThumbprint
if (-not $thumbprint) { throw 'EXPECTED_THUMBPRINT_REQUIRED' }

if ($Mode -eq 'Sign') {
    $certificate = Resolve-Certificate $thumbprint
    $thumbprint = Normalize-Thumbprint $certificate.Thumbprint
    $arguments = @(
        'sign', '/v', '/s', 'My', '/sha1', $thumbprint,
        '/fd', 'SHA256', '/tr', $timestampUrl, '/td', 'SHA256',
        '/d', $Description
    ) + @($files.FullName)
    $signResult = Invoke-Native $tool $arguments
    if ($signResult.ExitCode -ne 0) {
        throw "SIGNTOOL_SIGN_FAILED: exit $($signResult.ExitCode)`n$($signResult.Output -join [Environment]::NewLine)"
    }
}

$checks = @($files | ForEach-Object { Test-SignedFile $_ $thumbprint $tool })
$invalid = @($checks | Where-Object { -not $_.Valid })
$report = [pscustomobject]@{
    Mode = $Mode
    GeneratedAt = (Get-Date).ToString('o')
    User = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    SessionId = $sessionId
    SignToolPath = $tool
    ExpectedSignerThumbprint = $thumbprint
    FileCount = $checks.Count
    ValidCount = $checks.Count - $invalid.Count
    Files = $checks
}

if ($ReportPath) {
    if ($ReportPath -notmatch '^[Dd]:\\KEMI-Test\\') {
        throw "D_DRIVE_BOUNDARY_VIOLATION: $ReportPath"
    }
    $reportDirectory = Split-Path -Parent $ReportPath
    if ($reportDirectory) { New-Item -ItemType Directory -Force -Path $reportDirectory | Out-Null }
    $report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $ReportPath -Encoding UTF8
}

$report | ConvertTo-Json -Depth 6
if ($invalid.Count -gt 0) {
    throw "SIGNATURE_VERIFICATION_FAILED: $($invalid.Count) of $($checks.Count) file(s) failed status, signer, timestamp, or SignTool verification."
}
