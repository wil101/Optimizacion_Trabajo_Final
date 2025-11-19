@echo off
echo ================================================================================
echo   INSTALADOR DE DEPENDENCIAS - SOLUCIONADOR DE PROGRAMACION LINEAL
echo ================================================================================
echo.
echo Este script instalara las dependencias necesarias para ejecutar la aplicacion.
echo.
echo Presiona cualquier tecla para continuar o Ctrl+C para cancelar...
pause > nul
echo.
echo Instalando dependencias...
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor, instala Python 3.7 o superior desde https://www.python.org
    pause
    exit /b 1
)

echo Python detectado correctamente.
echo.
echo Instalando numpy y matplotlib...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Hubo un problema al instalar las dependencias
    echo Intenta instalar manualmente con: pip install numpy matplotlib
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo   INSTALACION COMPLETADA EXITOSAMENTE!
echo ================================================================================
echo.
echo Ya puedes ejecutar el programa con: python mian.py
echo.
echo Archivos disponibles:
echo   - mian.py: Programa principal
echo   - README.md: Documentacion completa
echo   - ejemplos_casos_prueba.py: Casos de prueba
echo   - INICIO_RAPIDO.txt: Guia rapida
echo.
echo Presiona cualquier tecla para salir...
pause > nul
