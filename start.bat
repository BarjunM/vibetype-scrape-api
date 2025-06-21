@echo off
echo Starting Web Content Parser API...
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your OpenAI API key.
    echo.
    pause
    exit /b 1
)

REM Start the API server
echo Starting server at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python main.py
