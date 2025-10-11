
pushd "%~dp0"
set "SCRIPT_DIR=%~dp0"
echo Script folder: %~dp0
echo Current folder: %CD%

call "%SCRIPT_DIR%Scripts\activate.bat"
timeout /T 1 /NOBREAK >nul
start "API_Module" cmd /k "cd /d "%SCRIPT_DIR%" && "%SCRIPT_DIR%Scripts\python.exe" "%SCRIPT_DIR%main.py""
start "WebServer" cmd /k "cd /d "%SCRIPT_DIR%" && "%SCRIPT_DIR%Scripts\python.exe" "%SCRIPT_DIR%web_server.py""

timeout /T 5 /NOBREAK >nul

start "" "http://127.0.0.1:8000/"

popd
