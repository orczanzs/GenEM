@echo off
title GenEM indito
chcp 65001 >nul

:: Mindig a .bat saját mappájába lép
cd /d "%~dp0"

:: Asztali parancsikon elérési útja
set shortcut=%USERPROFILE%\Desktop\GenEM.lnk

:: Ha nincs parancsikon, hozzuk létre
if not exist "%shortcut%" (
    powershell -NoLogo -NoProfile -Command ^
    "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%shortcut%'); $s.TargetPath = '%~dp0genem.bat'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0GenEM.ico'; $s.Save()"
)

:START
python main.py

echo.
echo A GenEM futása befejeződött.
echo Nyomj egy gombot az újraindításhoz, vagy zárd be az ablakot.
pause >nul
goto START
