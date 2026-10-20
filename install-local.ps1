# Modified for the local English edition, 2026-10-20.
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string[]]$Skill,
    [string]$Destination
)
$ErrorActionPreference = 'Stop'

if (-not $Destination) {
    $configRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
    $Destination = Join-Path $configRoot 'skills'
}
$sourceRoot = Join-Path $PSScriptRoot 'skills'
$destinationProvider = $null
$destinationDrive = $null
$destinationRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination, [ref]$destinationProvider, [ref]$destinationDrive)
if ($destinationProvider.Name -ne 'FileSystem') { throw 'Destination must be a filesystem directory.' }
$sourceAbsolute = [IO.Path]::GetFullPath($sourceRoot)
if (($destinationRoot -eq $sourceAbsolute) -or $destinationRoot.StartsWith($sourceAbsolute + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Choose an installation destination outside the package source skills directory.'
}
$available = @(Get-ChildItem -LiteralPath $sourceRoot -Directory | Select-Object -ExpandProperty Name)
if (-not $Skill) { $Skill = $available }
$selected = @($Skill + 'nature-shared' | Sort-Object -Unique)
$plan = @()
foreach ($name in $selected) {
    if ($name -notin $available) { throw "Unknown skill directory: $name" }
    $targetName = if ($name -eq 'nature-proposal-writer') { 'researchwrite' } else { $name }
    $source = Join-Path $sourceRoot $name
    $target = Join-Path $destinationRoot $targetName
    if (Test-Path -LiteralPath $target) { throw "Destination already exists; no files copied: $target" }
    if (($name -ne $targetName) -and (Test-Path -LiteralPath (Join-Path $destinationRoot $name))) {
        throw "An alternate installation already exists; no files copied: $name"
    }
    $plan += [pscustomobject]@{ Source = $source; Target = $target }
}

foreach ($item in $plan) {
    if ($PSCmdlet.ShouldProcess($item.Target, 'Copy complete English-edition skill directory')) {
        if (-not (Test-Path -LiteralPath $destinationRoot)) {
            New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null
        }
        Copy-Item -LiteralPath $item.Source -Destination $item.Target -Recurse -ErrorAction Stop
        Write-Output "Installed: $($item.Target)"
    }
}
