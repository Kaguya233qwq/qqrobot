@echo off
echo Starting qq_login/go-cqhttp.exe...
cd qq_login
%Created by go-cqhttp. DO NOT EDIT ME!%
start cmd /K "go-cqhttp.exe"
cd ..
echo Attempting to run main.py...
echo Dont close this window !!!
python main.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run main.py, installing requests package...
    pip install requests
    echo Attempting to run main.py again...
    python main.py
)