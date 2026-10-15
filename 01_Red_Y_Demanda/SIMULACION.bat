@echo off
chcp 65001 > nul

set "SUMO_HOME=C:\SUMO"
set "XML2CSV=C:\SUMO\tools\xml\xml2csv.py"
set "RED_DIR=C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda"
set "XML_DIR=C:\Users\samue_yffy\Desktop\SUMO\02_Resultados_Base"
set "CSV_DIR=C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS"

echo ==========================================
echo   Iniciando Simulación de la Costanera
echo   Escenario base: hora pico 2026
echo ==========================================

:: Abre SUMO y ESPERA a que lo cierres (los XML se terminan de escribir al cerrar SUMO)
:: --random: cada corrida usa una semilla distinta (resultados un poco diferentes cada vez)
start "" /wait "C:\SUMO\bin\sumo-gui.exe" -c "%RED_DIR%\tesis_base.sumocfg" --random

echo.
echo Convirtiendo resultados a CSV...

for %%N in (reporte_viajes reporte_colas reporte_densidad) do (
    echo Convirtiendo %%N.xml a CSV...
    python "%XML2CSV%" "%XML_DIR%\%%N.xml" -o "%CSV_DIR%\%%N.csv"
    if errorlevel 1 (
        echo ERROR al convertir %%N.xml
        pause
        exit /b 1
    )
)

echo Calculando niveles de servicio por intersección...
python "%RED_DIR%\herramientas\resumen_resultados.py" base2026 "%XML_DIR%" "%CSV_DIR%"
if errorlevel 1 (
    echo ERROR al calcular el resumen de intersecciones
    pause
    exit /b 1
)

echo.
echo ¡Proceso terminado! Abriendo Excel de Análisis...

:: Abrir maximizado
start /max excel "%CSV_DIR%\RESULTADOS SIMULACION.xlsm"

exit
