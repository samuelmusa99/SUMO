@echo off
chcp 65001 > nul

set "SUMO_HOME=C:\SUMO"
set "RED_DIR=C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda"
set "XML_DIR=C:\Users\samue_yffy\Desktop\SUMO\02_Resultados_Base"
set "CSV_DIR=C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS"

echo ==========================================
echo   Simulación de la Costanera
echo   Horizonte 2041 sin proyecto (demanda 2026 x 1,448)
echo ==========================================
echo.
echo Corriendo 5 réplicas sin ventana (puede tardar unos 10 minutos)...
python "%RED_DIR%\herramientas\replicas.py" 5 "%RED_DIR%\escenario_2041.sumocfg" "%XML_DIR%" "%CSV_DIR%" resumen_replicas_2041.csv
if errorlevel 1 (
    echo ERROR al correr las réplicas de 2041
    pause
    exit /b 1
)

echo.
echo ¡Proceso terminado! Abriendo Excel de Análisis...
start /max excel "%CSV_DIR%\RESULTADOS SIMULACION.xlsm"

exit