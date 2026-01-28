import os
import sys
import time
import pytest
from selenium import webdriver
import pandas as pd
from pytest_metadata.plugin import metadata_key
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from amazonAssignment.utilities.read_properties import Read_Config  # Added import
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Specify the Browser: Chrome, firefox or Edge")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browser in headless mode")

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture()
def headless(request):
    return request.config.getoption("--headless")

@pytest.fixture()
def setup(browser, headless):
    driver = None
    try:
        if browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(options=chrome_options)
        elif browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            firefox_options = Options()
            if headless:
                firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(options=firefox_options)
        elif browser == "edge":
            from selenium.webdriver.edge.options import Options
            edge_options = Options()
            if headless:
                edge_options.add_argument("--headless")
            driver = webdriver.Edge(options=edge_options)
        else:
            raise ValueError(f"Unsupported Browser: {browser}")

        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        pytest.fail(f"Browser initialization failed: {str(e)}")

def pytest_configure(config):
    # Initialize configuration first
    try:
        config.stash[metadata_key] = {
            'Project Name': 'Lambda Test Assignment',
            'Test Module Name': 'UI Functional Tests',
            'Tester Name': 'Atharva Hiwase',
        }
        logger.info("Pytest configuration initialized successfully")
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise

@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop('JAVA_HOME', None)
    metadata.pop('Plugins', None)
    metadata.pop('Packages', None)

def is_pycharm_debug():
    """Check if running in PyCharm debug mode"""
    return 'pydevd' in sys.modules or os.getenv('PYCHARM_DEBUG', '0') == '1'

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    """Early validation of test environment"""
    try:
        # Verify critical configurations are present
        #assert Read_Config.get_auth_url(), "Authentication URL not configured"
        assert Read_Config.get_amazon_url(), "Application URL not configured"
    except AssertionError as e:
        logger.error(f"Configuration error: {e}")
        pytest.exit(f"Aborting tests: {e}")