
python -m venv $PSScriptRoot
Set-Location $PSScriptRoot\Scripts
.\Activate.ps1
Write-Host $PSScriptRoot
.\pip.exe install -r ..\requirements.txt
