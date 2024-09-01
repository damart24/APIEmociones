@echo off
REM Comprueba si Python está instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python no está instalado. Instalando Python solo para el usuario actual...

    REM Ejecuta el instalador de Python en modo silencioso, añadiendo Python al PATH, instalando el Python Launcher y asociando archivos .py
    python-3.9.13-amd64.exe /quiet PrependPath=1 AssociateFiles=1

    REM Verifica si la instalación fue exitosa
    python --version >nul 2>&1
    IF ERRORLEVEL 1 (
        echo La instalación de Python falló. Esto puede deberse a:
        echo - Permisos insuficientes para realizar la instalación.
        echo - El instalador está corrupto.
        echo - Otra instancia de Python está corriendo.
        echo Por favor, intenta instalarlo manualmente o revisa los permisos del instalador.
        pause
        exit /b
    )
) ELSE (
    echo Python ya está instalado.
)

REM Comprueba si pip está disponible
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Pip no está instalado. Instalando pip...
    python -m ensurepip --upgrade
)

REM Comprueba si requirements.txt existe
IF NOT EXIST requirements.txt (
    echo El archivo requirements.txt no se encuentra en el directorio actual.
    pause
    exit /b
)

REM Instala las dependencias
pip install -r requirements.txt

REM Pausa para que la ventana no se cierre inmediatamente
echo Instalación completa. Presiona cualquier tecla para continuar...
pause >nul
