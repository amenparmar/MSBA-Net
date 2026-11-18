# Suspends (-Action suspend) or resumes (-Action resume) the running KolektorSDD2 training processes (ksdd2.py),
# so that latency can be timed on an idle GPU. Uses ntdll NtSuspendProcess / NtResumeProcess.
param([Parameter(Mandatory=$true)][ValidateSet("suspend","resume")][string]$Action)
Add-Type -Namespace W -Name Nt -MemberDefinition @"
[DllImport("ntdll.dll")] public static extern int NtSuspendProcess(IntPtr h);
[DllImport("ntdll.dll")] public static extern int NtResumeProcess(IntPtr h);
"@
$procs = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'ksdd2\.py' }
foreach ($p in $procs) {
  $h = (Get-Process -Id $p.ProcessId).Handle
  if ($Action -eq "suspend") { $r = [W.Nt]::NtSuspendProcess($h) } else { $r = [W.Nt]::NtResumeProcess($h) }
  Write-Output "$Action $($p.ProcessId) -> $r"
}
if (-not $procs) { Write-Output "no ksdd2.py process found" }
