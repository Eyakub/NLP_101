from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import pandas as pd


def fetching_number(str_no):
    pattern = re.compile(r"\b0[\d-]{7,}\b")

    match = pattern.search(str_no)
    if match:
        phone_number = match.group()
        print("Extracted phone number:", phone_number)
    else:
        phone_number = None
        print("No phone number found.")
    return phone_number


def chrome_options():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-cache")
    options.add_argument("--incognito")
    return options

def shop_numbers(g_url, msg):
    opt = chrome_options()
    driver = webdriver.Chrome(options=opt)
    driver.get(g_url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(msg)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # click on recaptcha
    recaptcha_btn = driver.find_element(By.CLASS_NAME, "g-recaptcha")
    action = ActionChains(driver)
    action.move_to_element(recaptcha_btn).click().perform()
    time.sleep(20)
    more_btn = driver.find_element(By.TAG_NAME, "g-more-link")
    action.move_to_element(more_btn).click().perform()

    shop_info = []

    while len(shop_info) < 100:
        try:
            results = driver.find_elements(By.XPATH, "//div[contains(@class, 'VkpGBb')]")
            for result in results:
                
                shop_name = result.find_element(By.CLASS_NAME, "dbg0pd")
                shop_no = result.find_element(By.CSS_SELECTOR, "div > a > div > div > div:nth-child(4)")
                shop_no = fetching_number(shop_no.text)
                if shop_no:
                    shop_info.append({
                        "shop_name": shop_name.text,
                        "shop_no": shop_no
                    })
        except Exception as e:
            print(f"Error occurred: {e}")

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".d6cvqb.BBwThe > a#pnnext")
            print("Next button: ", next_button)
            next_button.click()
            wait.until(EC.staleness_of(results[0]))
        except Exception as e:
            print(f"No more needed...{e}")

    driver.quit()
    return pd.DataFrame(shop_info)


if __name__ == '__main__':
    url = "https://www.google.com/"
    user_input = input("Enter your search message (leave empty for default 'Laptop shop near Mirpur'): ")
    user_msg = user_input if user_input else "Laptop shop near Mirpur"

    numbers = shop_numbers(url, user_msg)
    numbers.to_csv("shop_numbers.csv", index=False)
