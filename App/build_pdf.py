import subprocess
import yaml
import shutil
from pathlib import Path
from jinja2 import Environment
import os

def run_cmd(command, logger=print):
    logger(f"Running: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    for line in iter(process.stdout.readline, ''):
        if line.strip():
            logger(line.strip())
    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)

def convert_md_to_tex(md_file, tex_file, logger=print):
    # create tex_file if it does not exist
    tex_file = Path(tex_file)
    if not tex_file.parent.exists():
        tex_file.parent.mkdir(parents=True, exist_ok=True)
    run_cmd(["pandoc", md_file, "-o", str(tex_file), "--to=latex"], logger=logger)

def generate_main_tex(metadata_file, template, output_file, logger=print):
    with open(metadata_file) as f:
        metadata = yaml.safe_load(f)
    if template == "Main": 
        template_file = Path("App/layout/main_template.tex").resolve()
    with open(template_file) as f:
        template_content = f.read()
    
    env = Environment(
        block_start_string="((*",
        block_end_string="*))",
        variable_start_string="((",
        variable_end_string="))",
        comment_start_string="((#",
        comment_end_string="#))"
    )
    
    template = env.from_string(template_content)
    rendered = template.render(**metadata)

    with open(output_file, "w") as f:
        f.write(rendered)
    
    logger(f"Generated {output_file} from {Path(metadata_file).name} and {Path(template_file).name}")

def compile_latex(main_tex, output_dir, app_dir, logger=print):
    # copy classes to output directory
    shutil.copytree(os.path.join(app_dir,"classes"), os.path.join(output_dir, "classes"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(app_dir,"layout"), os.path.join(output_dir,  "layout"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(app_dir,"logos"), os.path.join(output_dir, "logos"), dirs_exist_ok=True)
    os.chdir(output_dir)
    run_cmd([
        "latexmk",
        "-pdf",
        "-pdflatex=pdflatex -interaction=nonstopmode",
        "-f",
        os.path.join(output_dir,main_tex)
    ], logger=logger)

def cleanup_aux_files(temp, output_dir, logger=print):
    os.chdir(Path(output_dir).parent)
    shutil.copy(os.path.join(temp, "main.pdf"), os.path.join(output_dir, "main.pdf"))
    shutil.rmtree(temp, ignore_errors=True)
    logger(f"Cleaned up auxiliary files in {output_dir}")

