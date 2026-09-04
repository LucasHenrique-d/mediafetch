from PyInstaller.utils.hooks import collect_all


APP_NAME = "MediaFetch"
ICON_PATH = "assets/icon.ico"


datas = []
binaries = []
hiddenimports = []


# ============================================================
# yt-dlp
# ============================================================

yt_dlp_datas, yt_dlp_binaries, yt_dlp_hiddenimports = (
    collect_all("yt_dlp")
)

datas += yt_dlp_datas
binaries += yt_dlp_binaries
hiddenimports += yt_dlp_hiddenimports


# ============================================================
# ASSETS
# ============================================================

datas += [
    (
        "assets",
        "assets",
    )
]


# ============================================================
# APLICAÇÃO
# ============================================================

a = Analysis(
    ["launcher.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)


pyz = PYZ(
    a.pure,
)


# ============================================================
# EXECUTÁVEL
# ============================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=ICON_PATH,
)