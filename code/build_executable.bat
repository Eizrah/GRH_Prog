@echo off
echo ==========================================
echo      GENERATION DE L'EXECUTABLE GRH
echo ==========================================

cd /d "%~dp0"

echo Installation de PyInstaller si necessaire...
pip install pyinstaller

echo.
echo Nettoyage des anciens builds...
rmdir /s /q build
rmdir /s /q dist
del /q *.spec

echo.
echo Lancement de PyInstaller...
echo Incluant: database -> database
echo.

pyinstaller --noconsole --onefile ^
    --name "GRH_Application" ^
    --add-data "database;database" ^
    --hidden-import "babel.numbers" ^
    --hidden-import "tkcalendar" ^
    --hidden-import "PIL" ^
    --hidden-import "customtkinter" ^
    main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo SUCCES ! L'executable est dans le dossier 'dist'
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo ECHEC de la generation.
    echo ==========================================
)
pause
