@echo off
chcp 65001 > nul

set "XML2CSV=C:\SUMO\tools\xml\xml2csv.py"
set "XML_DIR=C:\Users\samue_yffy\Desktop\SUMO\02_Resultados_Base"
set "CSV_DIR=C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS\PROPUESTA_PEROZO"

echo ==========================================
echo   Iniciando Simulación de la Costanera
echo ==========================================

:: Abre SUMO y ESPERA a que lo cierres (los XML se terminan de escribir al cerrar SUMO)
start "" /wait "C:\SUMO\bin\sumo-gui.exe" -c "C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda\tesis_base.sumocfg" --random

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

echo.
echo ¡Proceso terminado! Abriendo Excel de Análisis...

:: Abrir maximizado
start /max excel "%CSV_DIR%\RESULTADOS SIMULACION.xlsm"

exit
