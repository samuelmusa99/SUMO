@echo off
chcp 65001 > nul

set "SUMO_HOME=C:\SUMO"
set "XML2CSV=C:\SUMO\tools\xml\xml2csv.py"
set "RED_DIR=C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda"
set "XML_DIR=C:\Users\samue_yffy\Desktop\SUMO\02_Resultados_2041"
set "CSV_DIR=C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS\PROPUESTA_FINAL\2041"
:: resumen de la propuesta en 2026: de ahi se toma la capacidad de cada acceso (la via y los semaforos son los mismos)
set "BASE_2026=C:\Users\samue_yffy\Desktop\EXCEL RESULTADOS\PROPUESTA_FINAL\2026\resumen_replicas.csv"

echo ==========================================
echo   Simulación de la Costanera
echo   Propuesta Final: horizonte 2041 (demanda 2026 x 1,448)
echo ==========================================

:: Abre SUMO y ESPERA a que lo cierres (los XML se terminan de escribir al cerrar SUMO)
:: --random: cada corrida usa una semilla distinta (resultados un poco diferentes cada vez)
start "" /wait "C:\SUMO\bin\sumo-gui.exe" -c "%RED_DIR%\escenario_2041.sumocfg" --random

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
python "%RED_DIR%\herramientas\resumen_resultados.py" final2041 "%XML_DIR%" "%CSV_DIR%"
if errorlevel 1 (
    echo ERROR al calcular el resumen de intersecciones
    pause
    exit /b 1
)

echo.
echo Corriendo 5 réplicas sin ventana para promediar resultados (unos 10 minutos)...
python "%RED_DIR%\herramientas\replicas.py" 5 "%RED_DIR%\escenario_2041.sumocfg" "%XML_DIR%" "%CSV_DIR%" resumen_replicas.csv "%BASE_2026%"
if errorlevel 1 (
    echo ERROR al correr las réplicas
    pause
    exit /b 1
)

echo.
echo ¡Proceso terminado! Abriendo Excel de Análisis 2041...

:: Abrir maximizado
start /max excel "%CSV_DIR%\RESULTADOS FINAL 2041.xlsm"

exit
