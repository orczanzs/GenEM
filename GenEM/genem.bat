@echo off
title GenEM indito

:: A .bat sajat mappajaba lep
cd /d "%~dp0"

:: Ellenorzes: main.py letezik-e
if not exist "main.py" (
    echo Hiba: A main.py nem talalhato a GenEM mappaban!
    echo Győződj meg róla, hogy a .bat és a main.py ugyanabban a mappában van.
    pause
    exit /b
)

:: Program inditasa
echo GenEM inditasa...
python main.py

echo.
echo A program futasa befejezodott.
pause
