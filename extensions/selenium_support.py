import sys
import os
import platform
from selenium import webdriver as _webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

def get_app_dir():
    # When frozen by PyInstaller, binaries are extracted to _MEIPASS
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_chromedriver_path():
    base_path = get_app_dir()
    driver_dir = os.path.join(base_path, "extensions", "chrome_drivers")

    system = platform.system().lower()
    if system == "windows":
        driver_name = "chromedriver-win.exe"
    elif system == "darwin":
        driver_name = "chromedriver-macos"
    else:
        driver_name = "chromedriver-linux"

    return os.path.join(driver_dir, driver_name)

_original_chrome_init = _webdriver.Chrome.__init__

def _patched_chrome_init(self, *args, **kwargs):
    if 'service' not in kwargs:
        kwargs['service'] = ChromeService(executable_path=get_chromedriver_path())
    _original_chrome_init(self, *args, **kwargs)

_webdriver.Chrome.__init__ = _patched_chrome_init

patched_webdriver = _webdriver
patched_options = Options
