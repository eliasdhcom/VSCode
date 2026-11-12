############################
# @author EliasDH Team     #
# @see https://eliasdh.com #
# @since 12/11/2026        #
############################
# Installs the EliasDH theme in VS Code and activates it.
# Usage: irm https://raw.githubusercontent.com/eliasdhcom/VSCode/main/install.ps1 | iex

& {
    Write-Host ''
    Write-Host 'Choose a theme:' -ForegroundColor Cyan
    Write-Host '  1) EliasDH Dark'
    Write-Host '  2) EliasDH Light'
    $choice = Read-Host 'Enter 1 or 2 (default 1)'
    $themeName = if ($choice.Trim() -eq '2') { 'EliasDH Light' } else { 'EliasDH Dark' }
    $ErrorActionPreference = 'Stop'
    $ProgressPreference = 'SilentlyContinue'
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $repo = 'https://raw.githubusercontent.com/eliasdhcom/VSCode/main'

    # 1. Find VS Code
    $code = (Get-Command code -ErrorAction SilentlyContinue).Source
    if (-not $code) {
        $code = @(
            "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd",
            "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd"
        ) | Where-Object { Test-Path $_ } | Select-Object -First 1
    }
    if (-not $code) { Write-Host 'VS Code was not found. Install it from https://code.visualstudio.com first.' -ForegroundColor Red; return }

    # 2. Download the latest .vsix to a temp folder
    $pkg = Invoke-RestMethod "$repo/package.json" -UseBasicParsing
    if ($pkg -is [string]) { $pkg = $pkg | ConvertFrom-Json }
    $version = $pkg.version
    $vsix = Join-Path $env:TEMP "eliasdh-theme-$version.vsix"
    Write-Host "Downloading EliasDH theme $version..." -ForegroundColor Cyan
    Invoke-WebRequest "$repo/Release/eliasdh-theme-$version.vsix" -OutFile $vsix -UseBasicParsing

    # 3. Install it, then clean up
    $ErrorActionPreference = 'Continue'
    & $code --install-extension $vsix --force 2>&1 | Out-Null
    $installed = $LASTEXITCODE -eq 0
    $ErrorActionPreference = 'Stop'
    Remove-Item $vsix -Force -ErrorAction SilentlyContinue
    if (-not $installed) { Write-Host 'Installing the extension failed.' -ForegroundColor Red; return }

    # 4. Activate the theme in the user settings
    $dir = Join-Path $env:APPDATA 'Code\User'
    $settings = Join-Path $dir 'settings.json'
    $entry = "`"workbench.colorTheme`": `"$themeName`""
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $json = if (Test-Path $settings) { [IO.File]::ReadAllText($settings) } else { '' }
    if ([string]::IsNullOrWhiteSpace($json)) { $json = "{`n}`n" }
    $pattern = '"workbench\.colorTheme"\s*:\s*"[^"]*"'
    if ($json -match $pattern) { $json = $json -replace $pattern, $entry }
    elseif ($json -match '^\s*\{') { $json = $json -replace '^\s*\{', "{`n    $entry," }
    else { Write-Host "Installed. Select `"$themeName`" with Ctrl+K Ctrl+T." -ForegroundColor Green; return }
    [IO.File]::WriteAllText($settings, $json, (New-Object Text.UTF8Encoding $false))

    Write-Host "$themeName installed and activated." -ForegroundColor Green
}
