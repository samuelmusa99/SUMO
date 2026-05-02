@echo off
chcp 65001 > nul

echo ==========================================
echo   Iniciando Simulación de la Costanera
echo ==========================================

:: 1. En lugar de buscar el programa, le decimos a Windows que "inicie" el archivo
:: Esto es exactamente lo mismo que cuando tú le dabas doble clic al tesis_base.sumocfg
start "" "C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda\tesis_base.sumocfg"

echo.
echo Esperando a que cierres SUMO para procesar datos...
echo (Presiona una tecla en esta ventana SOLO cuando hayas terminado la simulación)
pause

echo Convirtiendo resultados a CSV...

cd /d "C:\Users\samue_yffy\Desktop\SUMO\02_Resultados_Base"

python "C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda\xml2csv.py" reporte_viajes.xml
python "C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda\xml2csv.py" reporte_colas.xml
python "C:\Users\samue_yffy\Desktop\SUMO\01_Red_Y_Demanda\xml2csv.py" reporte_densidad.xml

echo.
echo ¡Proceso terminado! Abriendo Excel de Análisis...

echo ¡Proceso terminado! Abriendo Excel de Análisis...

:: Abrir maximizado
start /max excel "C:\Users\samue_yffy\Desktop\SUMO\03_Analsis_Excel\RESULTADOS SIMULACION.xlsm"

:: Cerramos la consola de inmediato para que Excel tome el control de la pantalla
exit