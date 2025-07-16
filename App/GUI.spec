# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import os

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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MD to LaTeX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    windowed=True,
    icon='logos\BUNDPDF.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
