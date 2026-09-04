@echo off
setlocal

echo ==========================================
echo        MediaFetch - Production Build
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual nao encontrado.
    echo.
    echo Execute:
    echo python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo [1/5] Verificando ambiente virtual...

.venv\Scripts\python.exe -c "import sys; print('Python:', sys.executable)"

if errorlevel 1 (
    echo.
    echo [ERRO] Python do ambiente virtual nao pode ser executado.
    pause
    exit /b 1
)

echo.

echo [2/5] Atualizando dependencias...

.venv\Scripts\python.exe -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.

echo [3/5] Verificando PyInstaller...

.venv\Scripts\python.exe -m PyInstaller --version

if errorlevel 1 (
    echo.
    echo [ERRO] PyInstaller nao esta instalado no ambiente virtual.
    echo.
    echo Execute:
    echo .venv\Scripts\python.exe -m pip install pyinstaller
    echo.
    pause
    exit /b 1
)

echo.

echo [4/5] Limpando builds anteriores...

if exist build (
    rmdir /s /q build
)

if exist dist (
    rmdir /s /q dist
)

echo.

echo [5/5] Gerando executavel...

.venv\Scripts\python.exe -m PyInstaller build.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar o executavel.
    pause
    exit /b 1
)

if not exist "dist\MediaFetch.exe" (
    echo.
    echo [ERRO] Executavel nao encontrado.
    pause
    exit /b 1
)

echo.

echo ==========================================
echo       BUILD CONCLUIDO COM SUCESSO!
echo ==========================================
echo.

echo Executavel:
echo dist\MediaFetch.exe

echo.

pause

endlocal