param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)
$ErrorActionPreference = "Stop"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git no esta instalado o no esta en PATH." }
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
if (-not (Test-Path ".git")) { git init }
git add .
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { git commit -m "Tiny Engineer ESP32-S3 N16R8 web installer" }
git branch -M main
git remote get-url origin 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) { git remote set-url origin $RepoUrl } else { git remote add origin $RepoUrl }
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw "git push fallo. Completa el login de GitHub si se abre el navegador y vuelve a ejecutar." }
Write-Host ""
Write-Host "Publicado. Activa una sola vez:"
Write-Host "Settings -> Pages -> Build and deployment -> Source -> GitHub Actions"
Write-Host "Despues espera a que termine el workflow de Pages."
