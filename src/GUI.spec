# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import os
import sys

# Utility to bundle folders
def folder_to_datas(folder_name):
    return [(os.path.join(folder_name, f), os.path.join(folder_name)) for f in os.listdir(folder_name)]

# Add folders here
data_folders = []
for folder in ["classes", "layout", "logos"]:
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path)
                dest_path = os.path.dirname(rel_path)
                data_folders.append((rel_path, dest_path))


a = Analysis(
    ['GUI.py'],
    pathex=[],
    binaries=[],
    datas=data_folders,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# Determine platform-specific values
if sys.platform == 'win32':
    icon_path = 'logos\\BUNDPDF.ico'
    windowed = True
    console = False
    target_name = 'MD2PDF.exe'
    argv_emulation = False
elif sys.platform == 'darwin':
    icon_path = 'logos/BUNDPDF.icns'
    windowed = True
    console = False
    target_name = 'MD2PDF'
    argv_emulation = True  # Needed on macOS for drag-and-drop support
elif sys.platform.startswith('linux'):
    icon_path = None  # Icons not typically used for CLI apps; optional .desktop files for GUI
    windowed = False  # No windowed mode by default
    console = True    # True if it's a CLI tool
    target_name = 'MD2PDF'
    argv_emulation = False
else:
    raise RuntimeError(f"Unsupported platform: {sys.platform}")

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name = target_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console= console,
    windowed= windowed,
    icon= icon_path,
    disable_windowed_traceback = False,
    argv_emulation = argv_emulation,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GUI',
)
