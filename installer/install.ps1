$ErrorActionPreference='Stop'
$Root=Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python=$env:PYTHON; if (-not $Python) {$Python='python'}
& $Python -m pip install --upgrade $Root
& $Python -m gene init
& $Python -m gene health
