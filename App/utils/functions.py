import os
import sys
import subprocess

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def check_command(command):
    """Check if command exists and works."""
    try:
        # On Windows, need shell=True for batch files like tlmgr
        result = subprocess.run([command, '--version'], 
                              capture_output=True, timeout=5, shell=True)
        return result.returncode == 0
    except:
        return False

def check_tinytex():
    """Check if TinyTeX is installed."""
    commands = ['latexmk', 'pdflatex', 'tlmgr']
    return all(check_command(cmd) for cmd in commands)

def check_pandoc():
    """Check if Pandoc is installed."""
    return check_command('pandoc')