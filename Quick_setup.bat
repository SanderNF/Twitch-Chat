set /p "Input1=Twitch client id: "
set /p "Input2=Twitch client secret: "
set /p "Input3=your channel name: "
set /p "Input4=max number big emotes: "
set /p "Input5=Your discord invite link: "

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


rem Create .env 
(
    echo client_id=%Input1%
    echo client_secret=%Input2%
    echo channel_name=%Input3%
    echo max_large_emotes=%Input4%
    echo discord_link=%Input5%
) > %SCRIPT_DIR%.env
