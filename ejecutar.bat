@echo off
echo ================================================================================
echo   SOLUCIONADOR DE PROGRAMACION LINEAL - METODO SIMPLEX REVISADO
echo ================================================================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor, instala Python 3.7 o superior desde https://www.python.org
    pause
    exit /b 1
)

python mian.py

if errorlevel 1 (
    echo.
    echo.
    echo ================================================================================
    echo   ERROR AL EJECUTAR EL PROGRAMA
    echo ================================================================================
    echo.
    echo Posibles causas:
    echo   1. No has instalado las dependencias (ejecuta instalar.bat primero)
    echo   2. Hay un error en el codigo
    echo.
    echo Si no has instalado las dependencias, ejecuta: instalar.bat
    echo O manualmente: pip install numpy matplotlib
    echo.
)

echo.
pause
