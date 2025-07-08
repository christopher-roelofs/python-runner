import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_chromedriver_path():
    options = Options()
    options.add_argument("--headless")
    service = Service()
    try:
        driver = webdriver.Chrome(service=service, options=options)
        path = service.path
        driver.quit()
        return path
    except Exception as e:
        print(f"❌ Error getting ChromeDriver path: {e}")
        return None

def build():
    chromedriver_path = get_chromedriver_path()
    if not chromedriver_path:
        print("❌ Failed to locate ChromeDriver path.")
        sys.exit(1)

    print(f"✅ Detected ChromeDriver path: {chromedriver_path}")

    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        f"--add-binary={chromedriver_path}:extensions/chrome_drivers",
        "runner.py"
    ]

    print("🔧 Running PyInstaller command:")
    print(" ".join(pyinstaller_cmd))

    subprocess.run(pyinstaller_cmd, check=True)

if __name__ == "__main__":
    build()
