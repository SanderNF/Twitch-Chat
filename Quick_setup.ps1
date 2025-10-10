$path = (Get-Item .).FullName
Write-Output $path
Write-Output $PSScriptRoot
python -m venv $PSScriptRoot
Set-Location $PSScriptRoot\Scripts
.\Activate.ps1
.\pip.exe install -r ..\requirements.txt


$answer = read-host "Do you wish to start the server on system bootup? (y/n) "
if ($answer -eq 'y') { 
    Write-Output 'Adding script to startup'


    # create startup rule

    $TaskAction1 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File $($PSScriptRoot)\Start_server.ps1"
    $TaskTrigger = New-ScheduledTaskTrigger -AtStartup
    $TaskPrincipal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    Register-ScheduledTask -Action $TaskAction1 -Trigger $TaskTrigger -Principal $TaskPrincipal -TaskName "Config" -Description "Config Script"
} elseif ($answer -eq 'n') {
    Write-Output 'To manualy start the server run the "Start_server.ps1" file'
}
..\Start_server.ps1
