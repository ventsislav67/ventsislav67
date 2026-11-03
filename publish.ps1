# Safe publishing helper for Windows PowerShell, no force push, no token in code.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$checkout = Join-Path $root 'profile-publish-worktree'

if (Test-Path $checkout) {
  Write-Host 'The profile-publish-worktree folder already exists. Review it and remove or rename it before re-running.' -ForegroundColor Yellow
  exit 1
}

Write-Host 'Cloning ventsislav67/ventsislav67...' -ForegroundColor Cyan
& git clone 'https://github.com/ventsislav67/ventsislav67.git' $checkout
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed. Check Git installation and repository access.' }

Copy-Item -LiteralPath (Join-Path $root 'README.md') -Destination (Join-Path $checkout 'README.md') -Force
$assetsDir = Join-Path $checkout 'assets'
$workflowDir = Join-Path $checkout '.github/workflows'
New-Item -ItemType Directory -Force -Path $assetsDir, $workflowDir | Out-Null
Copy-Item -Path (Join-Path $root 'assets/*') -Destination $assetsDir -Force
Copy-Item -LiteralPath (Join-Path $root '.github/workflows/profile-visuals.yml') -Destination (Join-Path $workflowDir 'profile-visuals.yml') -Force

Push-Location $checkout
try {
  Write-Host '`nFiles that will change:' -ForegroundColor Cyan
  & git status --short
  Write-Host '`nThe README.md will be replaced; other repository files remain intact.' -ForegroundColor Yellow
  $confirmation = Read-Host 'Type yes to commit and push the profile makeover'
  if ($confirmation -cne 'yes') {
    Write-Host 'No changes published. Review files in profile-publish-worktree.' -ForegroundColor Yellow
    exit 0
  }

  & git add -- README.md assets .github/workflows/profile-visuals.yml
  if ($LASTEXITCODE -ne 0) { throw 'Git add failed.' }
  & git diff --cached --quiet
  if ($LASTEXITCODE -eq 0) { Write-Host 'No changes to commit.'; exit 0 }

  & git commit -m 'feat(profile): animated neon README and automated stats'
  if ($LASTEXITCODE -ne 0) { throw 'Git commit failed. Configure git user.name and user.email.' }
  & git push
  if ($LASTEXITCODE -ne 0) { throw 'Git push failed. Changes are committed locally; check remote permissions before retrying.' }
  Write-Host 'Profile files published. Now run the workflow in the Actions tab.' -ForegroundColor Green
}
finally { Pop-Location }
