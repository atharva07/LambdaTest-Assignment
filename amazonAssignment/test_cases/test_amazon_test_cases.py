import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from amazonAssignment.utilities.get_test_data import get_test_data
from amazonAssignment.utilities.read_properties import Read_Config
from amazonAssignment.utilities.custom_logger import Log_maker
from amazonAssignment.basePages.BuyDeviceFlow import BuyDeviceFlow

class Test_amazon_test_cases:
    amazon_url = Read_Config.get_amazon_url()

    @pytest.mark.parametrize("testcase_id, execute_flag, test_type, test_case_description, device_name, model_name", get_test_data())
    def test_amazon_tests(self, testcase_id, execute_flag, test_type, test_case_description, device_name, model_name, request):
        # Check Execute_Flag before initializing anything
        if execute_flag.strip().upper() == 'N':
            pytest.skip(f"Skipping test case {testcase_id} as Execute_Flag is 'N'")

        # If test is not skipped, now request the 'setup' fixture
        setup = request.getfixturevalue("setup")

        logger = Log_maker.log_gen(testcase_id)
        logger.info("Driver is initiated")
        self.driver = setup
        self.driver.implicitly_wait(5)
        self.driver.get(self.amazon_url)
        self.driver.maximize_window()
        logger.info("Login Page is initiated")

        # Passing the driver object to login page constructor
        self.buyDevice = BuyDeviceFlow(self.driver)

        # Perform the actions
        price = self.buyDevice.select_product_process(device_name, model_name)

        logger.info(f"Product price for {device_name} {model_name} is: {price}")

        print("Driver to close")
        self.driver.quit()