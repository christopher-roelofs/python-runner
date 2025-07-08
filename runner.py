import os
import sys
import importlib.util
import traceback
import platform

# Import dependencies
from extensions import dependencies

def ensure_utills_folder():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running inside PyInstaller bundle
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as normal python script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    utills_path = os.path.join(base_dir, "utills")
    if not os.path.exists(utills_path):
        print(f"'utills' folder not found at {utills_path}, creating it.")
        os.makedirs(utills_path)
    return utills_path

def open_file_dialog():
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        if platform.system() == "Darwin":
            # macOS-specific focus handling
            root.lift()
            root.attributes("-topmost", True)
            root.after(100, lambda: root.focus_force())

        file_path = filedialog.askopenfilename(
            title="Select a Python Script to Run",
            filetypes=[("Python Files", "*.py")]
        )
        root.destroy()
        return file_path
    except Exception as e:
        print(f"[ERROR] Failed to open file dialog: {e}")
        return None

def load_and_run_script(script_path, script_args):
    globals_dict = {}
    exports = dependencies.get_exports()
    globals_dict.update(exports)

    globals_dict["__file__"] = script_path
    globals_dict["__name__"] = "__main__"

    sys.argv = [script_path] + script_args

    script_dir = os.path.dirname(os.path.abspath(script_path))
    utills_dir = ensure_utills_folder()
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    if utills_dir not in sys.path:
        sys.path.insert(0, utills_dir)

    try:
        spec = importlib.util.spec_from_file_location("__main__", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        print(f"[ERROR] Failed to run script: {script_path}")
        traceback.print_exc()

def main():
    ensure_utills_folder()

    if len(sys.argv) < 2:
        print("[INFO] No script file provided. Opening file browser...")
        script_file = open_file_dialog()
        if not script_file:
            print("[WARN] No file selected. Exiting.")
            sys.exit(0)
        script_args = []
    else:
        script_file = sys.argv[1]
        script_args = sys.argv[2:]

    if not os.path.isfile(script_file):
        print(f"[ERROR] Script file not found: {script_file}")
        sys.exit(1)

    load_and_run_script(script_file, script_args)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
