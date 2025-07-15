import subprocess
import shutil

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

def main():
    """Check both TinyTeX and Pandoc."""
    print("Checking installations...")
    
    tinytex_ok = check_tinytex()
    pandoc_ok = check_pandoc()
    
    print(f"TinyTeX: {'OK' if tinytex_ok else 'NOT FOUND'}")
    print(f"Pandoc: {'OK' if pandoc_ok else 'NOT FOUND'}")
    
    if tinytex_ok and pandoc_ok:
        print("All tools are installed.")
        return True
    else:
        print("Some tools are missing.")
        return False

if __name__ == "__main__":
    main()
