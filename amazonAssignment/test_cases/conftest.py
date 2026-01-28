import os
import sys
import pytest
import logging
from selenium import webdriver
from pytest_metadata.plugin import metadata_key

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from amazonAssignment.utilities.read_properties import Read_Config

# ---------------- LOGGING ---------------- #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- PYTEST OPTIONS ---------------- #
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser: chrome | firefox | edge")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browser in headless mode")
    parser.addoption("--env", action="store", default="local",
                     help="Execution environment: local | lambdatest")

@pytest.fixture
def browser(request):
    return request.config.getoption("--browser").lower()

@pytest.fixture
def headless(request):
    return request.config.getoption("--headless")

@pytest.fixture
def env(request):
    return request.config.getoption("--env").lower()

# ---------------- DRIVER FIXTURE ---------------- #
@pytest.fixture
def setup(browser, headless, env, request):
    driver = None

    try:
        # ========== LAMBDATEST EXECUTION ==========
        if env == "lambdatest":
            LT_USERNAME = os.getenv("LT_USERNAME")
            LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

            if not LT_USERNAME or not LT_ACCESS_KEY:
                pytest.exit("LambdaTest credentials are not set")

            grid_url = f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@hub.lambdatest.com/wd/hub"

            capabilities = {
                "browserName": browser.capitalize(),
                "browserVersion": "latest",
                "platformName": "Windows 10",
                "build": "LambdaTest Amazon Assignment",
                "name": request.node.name,
                "plugin": "python-pytest",
                "selenium_version": "4.15.0"
            }

            logger.info("Starting LambdaTest session")
            driver = webdriver.Remote(
                command_executor=grid_url,
                options=None,
                desired_capabilities=capabilities
            )

        # ========== LOCAL EXECUTION ==========
        else:
            logger.info("Starting Local browser session")

            if browser == "chrome":
                from selenium.webdriver.chrome.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                    options.add_argument("--window-size=1920,1080")
                driver = webdriver.Chrome(options=options)

            elif browser == "firefox":
                from selenium.webdriver.firefox.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)

            elif browser == "edge":
                from selenium.webdriver.edge.options import Options
                options = Options()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Edge(options=options)

            else:
                raise ValueError(f"Unsupported browser: {browser}")

        driver.implicitly_wait(10)
        yield driver

        # Mark test as passed in LambdaTest
        if env == "lambdatest":
            driver.execute_script("lambda-status=passed")

    except Exception as e:
        if driver and env == "lambdatest":
            driver.execute_script("lambda-status=failed")
        pytest.fail(f"Driver setup failed: {e}")

    finally:
        if driver:
            driver.quit()

# ---------------- METADATA ---------------- #
def pytest_configure(config):
    config.stash[metadata_key] = {
        "Project Name": "Lambda Test Assignment",
        "Test Module Name": "UI Functional Tests",
        "Tester Name": "Atharva Hiwase",
    }
    logger.info("Pytest metadata configured")

@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)

# ---------------- ENV VALIDATION ---------------- #
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    try:
        assert Read_Config.get_amazon_url(), "Amazon URL not configured"
    except AssertionError as e:
        pytest.exit(f"Configuration Error: {e}")
