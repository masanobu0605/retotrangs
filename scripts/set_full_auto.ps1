$ErrorActionPreference = 'Stop'

$path = 'C:\Users\masan\.codex\config.toml'

if (-not (Test-Path -LiteralPath $path)) {
  throw "Not found: $path"
}

$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
$bak = "$path.bak-$ts"
Copy-Item -LiteralPath $path -Destination $bak -Force

$text = Get-Content -LiteralPath $path -Raw

$regex = New-Object System.Text.RegularExpressions.Regex('(?ms)^\[approvals\]\s*(.*?)(?=^\[|\z)')
$m = $regex.Match($text)

if ($m.Success) {
  $section = $m.Value
  if ($section -match '(?m)^\s*policy\s*=') {
    $newSection = [System.Text.RegularExpressions.Regex]::Replace($section,'(?m)^\s*policy\s*=\s*"[^"]*"',"policy = `"full_auto`"")
  } else {
    $newSection = $section.TrimEnd() + "`r`n" + "policy = `"full_auto`"" + "`r`n"
  }
  $new = $text.Substring(0,$m.Index) + $newSection + $text.Substring($m.Index + $m.Length)
} else {
  $new = $text.TrimEnd() + "`r`n`r`n[approvals]`r`n" + "policy = `"full_auto`"" + "`r`n"
}

Set-Content -LiteralPath $path -Value $new -Encoding utf8

Write-Output "Backup: $bak"
Write-Output "Updated approvals block:"
Get-Content -LiteralPath $path | Select-String -Pattern '^\[approvals\]','^\s*policy\s*=','^\s*escalate_on','^\s*silent_for' | ForEach-Object { $_.Line }

