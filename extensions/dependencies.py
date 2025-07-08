import requests
import selenium
from .selenium_support import patched_webdriver as webdriver, patched_options as Options

def get_exports():
    return {
        "requests": requests,
        "selenium": selenium,
        "webdriver": webdriver,
        "Options": Options,
    }

def list_dependencies():
    return {
        "requests": requests.__version__,
        "selenium": selenium.__version__,
    }
