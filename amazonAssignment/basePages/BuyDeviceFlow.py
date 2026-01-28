import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BuyDeviceFlow:
    product_search_field_xpath = "//input[@aria-label='Search Amazon.in']"
    click_search_button_xpath = "//input[@id='nav-search-submit-button' and @type='submit']"
    product_price_xpath = "//h2[@class='a-size-base a-color-price a-text-bold']"
    add_to_cart_button = "(//input[@id='add-to-cart-button'])[2]"

    def __init__(self, driver):
        self.driver = driver

    def select_product_process(self, device_name, model_name):
        try:
            wait = WebDriverWait(self.driver, 10)
            # Search Product flow
            self.driver.find_element(By.XPATH, self.product_search_field_xpath).send_keys(device_name)
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.click_search_button_xpath).click()

            # Store current window
            parent_window = self.driver.current_window_handle

            wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{model_name}')]"))
            ).click()

            # Wait for new tab and switch
            wait.until(lambda d: len(d.window_handles) > 1)

            for window in self.driver.window_handles:
                if window != parent_window:
                    self.driver.switch_to.window(window)
                    break

            # add to cart flow
            self.driver.find_element(By.XPATH, self.add_to_cart_button).click()

            # Retrieve and print the price of the product
            total_amount = wait.until(
                EC.visibility_of_element_located((By.XPATH, self.product_price_xpath))
            ).text

            return total_amount

        except Exception as e:
            print(f"Error while selecting device: {e}")
            raise


