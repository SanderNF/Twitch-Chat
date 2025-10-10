$path = (Get-Item .).FullName
Write-Output $path
Write-Output $PSScriptRoot
Set-Location $PSScriptRoot
./Scripts/Activate.ps1
Start-Process PowerShell -ArgumentList .\main.py -WindowStyle Minimized
Start-Process PowerShell -ArgumentList .\web_server.py -WindowStyle Minimized
Start-Sleep -Seconds 5

Start-Process 'http://127.0.0.1:8000/'
