@echo off

echo ==========================================
echo Instagram Downloader - Release
echo ==========================================
echo.

call build_release.bat

if errorlevel 1 (
    echo.
    echo [ERRO] Build falhou.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Gerando instalador...
echo ==========================================
echo.

set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist %ISCC% (
    set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %ISCC% (
    echo [ERRO] Inno Setup nao encontrado.
    echo.
    echo Instale o Inno Setup ou ajuste o caminho.
    pause
    exit /b 1
)

if exist installer rmdir /s /q installer

mkdir installer

%ISCC% installer.iss

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar instalador.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo RELEASE GERADA COM SUCESSO!
echo ==========================================
echo.

dir installer

echo.
pause