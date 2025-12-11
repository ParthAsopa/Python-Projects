@echo off

:: Get the directory of this batch file
SET "BATCH_DIR=%~dp0"

:: Set the path to the venv's Python executable
SET "VENV_PYTHON=%BATCH_DIR%selenium_libs\Scripts\python.exe"

:: Set the path to your Python script
SET "PY_SCRIPT=%BATCH_DIR%WiFi_Login.py"

:: Run the script using the venv's Python
echo "--- Running your Python script with the venv ---"
"%VENV_PYTHON%" "%PY_SCRIPT%"

:: Keep the window open to see the output
echo.
echo "--- Script finished. Press any key to close. ---"
pause