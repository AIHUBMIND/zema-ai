# Batch script to add pip to PATH (Alternative method)
@echo off
setlocal

set "SCRIPTS_PATH=C:\Users\abrah\AppData\Local\Python\pythoncore-3.14-64\Scripts"

echo Checking if pip.exe exists...
if exist "%SCRIPTS_PATH%\pip.exe" (
    echo ✓ Found pip.exe at: %SCRIPTS_PATH%
    
    echo.
    echo Adding to User PATH...
    
    REM Add to current session PATH
    set "PATH=%PATH%;%SCRIPTS_PATH%"
    
    REM Add to User PATH permanently
    for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%B"
    
    echo %USER_PATH% | findstr /C:"%SCRIPTS_PATH%" >nul
    if errorlevel 1 (
        setx PATH "%USER_PATH%;%SCRIPTS_PATH%"
        echo ✓ Added %SCRIPTS_PATH% to PATH
    ) else (
        echo ⚠ Scripts folder is already in PATH!
    )
    
    echo.
    echo Testing pip...
    "%SCRIPTS_PATH%\pip.exe" --version
    
    echo.
    echo Note: You may need to restart your terminal for changes to take effect.
) else (
    echo ✗ pip.exe not found at: %SCRIPTS_PATH%
    echo Please check your Python installation path.
)

endlocal
pause

