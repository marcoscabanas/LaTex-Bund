import subprocess
import sys
import yaml
from pathlib import Path
from jinja2 import Environment
from pathlib import Path

def run_cmd(command):
    """Run shell command and stream output."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(command)}")
        sys.exit(result.returncode)

def convert_md_to_tex(md_file, tex_file):
    """Convert Markdown to LaTeX body fragment."""
    run_cmd([
        "pandoc",
        md_file,
        "-o", tex_file,
        "--to=latex"
    ])

def generate_main_tex(metadata_file, template_file, output_file):
    """Generate main.tex from metadata YAML and Jinja2 template."""
    with open(metadata_file) as f:
        metadata = yaml.safe_load(f)
    with open(template_file) as f:
        template_content = f.read()
    
    env = Environment(
        block_start_string='((*',
        block_end_string='*))',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='((#',
        comment_end_string='#))',
    )
    
    template = env.from_string(template_content)
    rendered = template.render(**metadata)
    
    with open(output_file, 'w') as f:
        f.write(rendered)
    
    print(f"Generated {output_file} from {metadata_file} and {template_file}.")

def compile_latex(main_tex):
    """Compile LaTeX file to PDF."""
    run_cmd([
        "latexmk",
        "-pdf",
        "-pdflatex=pdflatex -interaction=nonstopmode",
        "-f",
        main_tex
    ])

def cleanup_aux_files(tex_basename="main", extra_files=None):
    """Remove LaTeX auxiliary files and any additional files passed in."""
    extensions_to_remove = [".aux", ".fdb_latexmk", ".fls", ".tex"]
    files_to_remove = [Path(f"{tex_basename}{ext}") for ext in extensions_to_remove]

    # Add extra files if wanted
    if extra_files:
        files_to_remove.extend(Path(f) for f in extra_files)

    for path in files_to_remove:
        if path.exists():
            path.unlink()
            print(f"Deleted: {path}")
        else:
            print(f"Not found: {path}")


def main():
    md_file = "body.md"
    tex_file = "body.tex"
    metadata_file = "metadata.yaml"
    template_file = "layout/main_template_short.tex" #########################################################################
    main_tex = "main.tex"

    # Check files exist
    for file in [md_file, metadata_file, template_file]:
        if not Path(file).exists():
            print(f"Required file '{file}' not found.")
            sys.exit(1)

    convert_md_to_tex(md_file, tex_file)
    generate_main_tex(metadata_file, template_file, main_tex)
    compile_latex(main_tex)

    print("Build completed. Check your output PDF.")

if __name__ == "__main__":
    main()
    
    # Optional cleanup
    cleanup_aux_files("main", extra_files=["body.tex"])
