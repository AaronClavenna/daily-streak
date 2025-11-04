python .\log.py $args 

if ($LASTEXITCODE -eq 0) {
    git add .
    $today = Get-Date -Format "yyyy-MM-dd"
    $msg = if ($args.Count -gt 0) { $args -join " "} else { "Showed up." }
    git commit -m "log: $today - $msg"
    git push
} else {
    Write-Host "Skipping commit/push (exit code $LASTEXITCODE)."
}