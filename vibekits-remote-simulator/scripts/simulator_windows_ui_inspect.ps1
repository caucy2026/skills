param(
  [Parameter(Mandatory=$true)][int]$TargetPid,
  [Parameter(Mandatory=$true)][string]$ExpectedPath,
  [Parameter(Mandatory=$true)][string]$OutDirectory
)
$ErrorActionPreference='Stop'
$process=Get-Process -Id $TargetPid
if ($process.Path -ine $ExpectedPath) { throw 'PROCESS_IDENTITY_CHANGED' }
if ($process.SessionId -ne (Get-Process -Id $PID).SessionId) { throw 'WRONG_DESKTOP_SESSION' }
New-Item -ItemType Directory -Force $OutDirectory | Out-Null
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class VibeKitsWindowFocus {
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int n);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
}
'@
$condition=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::ProcessIdProperty),$TargetPid
$windows=[Windows.Automation.AutomationElement]::RootElement.FindAll([Windows.Automation.TreeScope]::Children,$condition)
$rows=@()
foreach($window in $windows){
 $handle=[IntPtr]$window.Current.NativeWindowHandle
 [VibeKitsWindowFocus]::ShowWindow($handle,9) | Out-Null
 [VibeKitsWindowFocus]::SetForegroundWindow($handle) | Out-Null
 $items=$window.FindAll([Windows.Automation.TreeScope]::Subtree,[Windows.Automation.Condition]::TrueCondition)
 for($i=0;$i -lt [Math]::Min(250,$items.Count);$i++){
  $item=$items[$i];$c=$item.Current
  if($c.IsPassword){continue}
  $rows+=@{name=$c.Name;controlType=$c.ControlType.ProgrammaticName;automationId=$c.AutomationId;enabled=$c.IsEnabled;offscreen=$c.IsOffscreen;processId=$c.ProcessId;bounds=@{x=$c.BoundingRectangle.X;y=$c.BoundingRectangle.Y;width=$c.BoundingRectangle.Width;height=$c.BoundingRectangle.Height}}
 }
}
@{pid=$TargetPid;path=$process.Path;sessionId=$process.SessionId;capturedAt=[DateTime]::UtcNow.ToString('o');windowCount=$windows.Count;nodes=$rows} | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $OutDirectory 'ui.json')
Start-Sleep -Milliseconds 700
$bounds=[Windows.Forms.SystemInformation]::VirtualScreen
$bitmap=New-Object Drawing.Bitmap $bounds.Width,$bounds.Height
$graphics=[Drawing.Graphics]::FromImage($bitmap)
try{
 $graphics.CopyFromScreen($bounds.Left,$bounds.Top,0,0,$bounds.Size)
 $bitmap.Save((Join-Path $OutDirectory 'focused.jpg'),[Drawing.Imaging.ImageFormat]::Jpeg)
}finally{$graphics.Dispose();$bitmap.Dispose()}
