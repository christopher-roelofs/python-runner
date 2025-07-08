import os
import sys
import importlib.util
import traceback

# Import dependencies from extensions package
from extensions import dependencies

def ensure_utills_folder():
    # Create 'utills' folder next to this runner.py (not in temp)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    utills_path = os.path.join(base_dir, "utills")
    if not os.path.exists(utills_path):
        print(f"'utills' folder not found at {utills_path}, creating it.")
        os.makedirs(utills_path)
    return utills_path

def load_and_run_script(script_path, script_args):
    # Prepare globals for script execution
    globals_dict = {}
    
    # Provide common libraries from dependencies.py exports
    exports = dependencies.get_exports()
    globals_dict.update(exports)

    # Add __file__ and __name__ for the script context
    globals_dict["__file__"] = script_path
    globals_dict["__name__"] = "__main__"

    # Adjust sys.argv for the script being run
    sys.argv = [script_path] + script_args

    # Add script folder and utills folder to sys.path for local imports
    script_dir = os.path.dirname(os.path.abspath(script_path))
    utills_dir = ensure_utills_folder()
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    if utills_dir not in sys.path:
        sys.path.insert(0, utills_dir)

    try:
        # Load the script as a module and execute it
        spec = importlib.util.spec_from_file_location("__main__", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        print(f"Error running script: {script_path}")
        traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Usage: runner.py <script.py> [args...]")
        print("Runs the specified Python script with shared dependencies.")
        sys.exit(1)

    script_file = sys.argv[1]
    script_args = sys.argv[2:]

    if not os.path.isfile(script_file):
        print(f"Script file not found: {script_file}")
        sys.exit(1)

    load_and_run_script(script_file, script_args)

if __name__ == "__main__":
    main()
