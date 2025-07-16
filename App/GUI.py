import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import os, sys
from utils.functions import get_resource_path
if sys.platform == "win32":
    from ctypes import windll
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass  # Fails silently on unsupported Windows versions

from build_pdf import convert_md_to_tex, generate_main_tex, compile_latex, cleanup_aux_files

class LaTeXProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX Document Processor")
        self.root.geometry("800x600")
        self.dir = Path(__file__).resolve().parent
        self.md_file = tk.StringVar(value = "-")
        self.metadata_file = tk.StringVar(value = "-")
        self.template_file_path = "-"
        self.template = tk.StringVar(value = "Full")
        self.output_dir = tk.StringVar(value = "-")
        self.cleanup_var = tk.BooleanVar(value = True)
        self.filename = tk.StringVar(value = "Bund Report")
        root.iconbitmap(get_resource_path(os.path.join("logos","BUNDPDF.ico")))

        self.is_processing = False

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        file_frame = ttk.LabelFrame(main_frame, text="File Selection")
        file_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        file_frame.columnconfigure(1, weight=1)

        self._add_file_input(file_frame, "Markdown File:", self.md_file, 0, "*.md")
        self._add_file_input(file_frame, "Metadata File:", self.metadata_file, 1, "*.yaml")
        self._add_dir_input(file_frame, "Output Directory:", self.output_dir, 2)
        self._add_output_name(file_frame, "Output File Name:", self.filename, 3)
        self._chose_template(file_frame, "Template File:", self.template, 4)

        options_frame = ttk.LabelFrame(main_frame, text="Options")
        options_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Checkbutton(options_frame, text="Clean up auxiliary files", variable=self.cleanup_var).grid(row=0, column=0, sticky="w")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.process_button = ttk.Button(button_frame, text="Process Document", command=self.start_processing)
        self.process_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_processing, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=5)

        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        log_frame = ttk.LabelFrame(main_frame, text="Output Log")
        log_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky="nsew")

    def _add_output_name(self, frame, label, var, row):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=var).grid(row=row, column=1, sticky="ew", pady=2)

    def _chose_template(self, frame, label, var, row):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Combobox(frame, textvariable=var, values=["Full", "Short"]).grid(row=row, column=1, sticky="ew", pady=2)
    
    def _add_file_input(self, frame, label, var, row, filetype):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=var).grid(row=row, column=1, sticky="ew", pady=2)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_file(var, filetype)).grid(row=row, column=2, pady=2)

    def _add_dir_input(self, frame, label, var, row):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=var).grid(row=row, column=1, sticky="ew", pady=2)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_dir(var)).grid(row=row, column=2, pady=2)

    def browse_file(self, var, pattern):
        f = filedialog.askopenfilename(filetypes=[("File", pattern), ("All files", "*.*")])
        if f:
            var.set(f)

    def browse_dir(self, var):
        d = filedialog.askdirectory()
        if d:
            var.set(d)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def start_processing(self):
        if self.is_processing:
            return
        self.temp_output_dir = os.path.join(self.output_dir.get(), "temp_LaTeX")
        # Validate files
        for f in [self.md_file.get(), self.metadata_file.get()]:
            if not Path(f).exists():
                messagebox.showerror("Missing File", f"File not found:\n{f}")
                return

        self.is_processing = True
        self.process_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress.start()

        thread = threading.Thread(target=self.process_document)
        thread.daemon = True
        thread.start()

    def stop_processing(self):
        self.is_processing = False
        self.log("Processing stopped by user.")
        self.finish_processing()

    def finish_processing(self):
        self.progress.stop()
        self.process_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.is_processing = False

    def process_document(self):
        try:
            md = Path(self.md_file.get()).resolve()
            meta = Path(self.metadata_file.get()).resolve()
            # tmpl = Path(self.template_file_path).resolve()

            self.log("Step 1: Converting Markdown to LaTeX...")
            body_tex = os.path.join(self.temp_output_dir, "body.tex")
            convert_md_to_tex(str(md), body_tex, logger=self.log)

            self.log("Step 2: Generating main.tex from template...")
            generate_main_tex(str(meta), self.template.get(), os.path.join(self.temp_output_dir,"main.tex"), logger=self.log)

            self.log("Step 3: Compiling LaTeX...")
            compile_latex("main.tex", self.temp_output_dir, self.dir, logger=self.log)
            if self.cleanup_var.get():
                self.log("Step 4: Cleaning up files...")
                cleanup_aux_files(self.temp_output_dir, self.output_dir.get(), self.dir, self.filename.get(), logger=self.log)

            self.log("✅ Document processed successfully.")
            messagebox.showinfo("Success", "Document processed successfully!")
        except Exception as e:
            self.log(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.root.after(0, self.finish_processing)

def main():
    root = tk.Tk()
    app = LaTeXProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
