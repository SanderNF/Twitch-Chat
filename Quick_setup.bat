
rem Batch equivalent of PowerShell's $PSScriptRoot
set "SCRIPT_DIR=%~dp0"

rem Print the script directory
echo %SCRIPT_DIR%

rem Create virtual environment in the script directory
python -m venv %SCRIPT_DIR%

rem Change to the venv Scripts folder
pushd %SCRIPT_DIR%Scripts || (echo Scripts folder not found & exit /b 1)

rem Activate the venv (Windows batch activation)
call %SCRIPT_DIR%Scripts\activate.bat

rem Print the script directory
echo %SCRIPT_DIR%

rem Install requirements
%SCRIPT_DIR%Scripts\pip.exe install -r %SCRIPT_DIR%\requirements.txt


rem Create .env with placeholders (escape < and >)
(
    echo client_id=^<your-app-id^>
    echo client_secret=^<your-app-secret^>
    echo channel_name=^<your-channel-name^>
) > %SCRIPT_DIR%.env
