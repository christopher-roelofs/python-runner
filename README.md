# Python Script Runner

A lightweight Python script runner executable that can run arbitrary Python scripts on machines **without Python installed**.\
It bundles common dependencies and provides support for:

- Passing command-line arguments to target scripts
- Running scripts with local imports (modules in the script’s folder)
- Shared utility modules located in a central `utills/` folder
- Relative file I/O by setting the working directory to the script’s folder
- Listing bundled dependencies and their versions

---

## Project Structure

```
project/
├── runner.py           # The main runner script (entry point)
├── dependencies.py     # Central place to import common dependencies
├── utills/             # Shared utility Python modules (no __init__.py yet)
│   ├── utils.py
│   ├── math_helpers.py
│   └── ...
├── scripts/            # Your Python scripts to run
│   ├── script1/
│   │   └── main.py
│   └── script2/
│       └── main.py
├── README.md
```

---

## How It Works

- `` imports your common Python libraries (e.g., `requests`, `numpy`, `Pillow`) so PyInstaller includes them in the bundled executable.
- ``:
  - Loads and runs a target Python script passed as a command-line argument.
  - Sets the working directory to the script’s folder to ensure relative file paths work correctly.
  - Adds the script’s folder and the shared `utills` folder to `sys.path` so local imports and shared utilities work seamlessly.
  - Sets `sys.argv` for the script to support passing arguments.
  - Provides a `--list` option to display bundled dependency versions.

---

## Usage

### Run a script

```bash
runner.exe path/to/script.py [arg1 arg2 ...]
```

Example:

```bash
runner.exe scripts/script1/main.py input.txt output.txt
```

This runs `main.py` with `sys.argv` set as if you ran:

```bash
python main.py input.txt output.txt
```

---

### List bundled dependencies

```bash
runner.exe --list
```

Output example:

```
requests: 2.31.0
numpy: 1.26.4
Image: 10.2.0
```

---

## How to add utilities

- Put reusable helper `.py` files into the `utills/` folder.
- Scripts can import them directly, e.g.:

```python
import utils
from math_helpers import add
```

No special setup required since `runner.py` adds `utills/` to `sys.path`.

---

## Building the executable

1. Install dependencies and PyInstaller in a clean virtual environment:

```bash
pip install pyinstaller requests numpy pillow
```

2. Build the runner executable:

```bash
pyinstaller --onefile runner.py
```

3. Distribute the `dist/runner.exe` along with your scripts and `utills/` folder.

---

## Notes

- The runner executes scripts using `exec()`, so do **not** run untrusted scripts.
- Scripts should use local imports or imports from `utills/` for helpers.
- Relative file paths in scripts work relative to the script file location.
- The `utills` folder currently does **not** use `__init__.py`, but you can add one to make it a package later.

---

## License

This project is released under the MIT License.

---

