from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd


def fetching_number(str_no):
    pattern = re.compile(r"\b0[\d-]{7,}\b")

    match = pattern.search(str_no)
    if match:
        phone_number = match.group()
        # print("Extracted phone number:", phone_number)
    else:
        phone_number = None
        print("No phone number found.")
    return phone_number


def laptop_shop_list(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    time.sleep(3)

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
    print("shop info: ", shop_info)
    return pd.DataFrame(shop_info)


if __name__ == '__main__':
    url = "https://www.google.com/search?sca_esv=f731f35a248a5872&tbm=lcl&sxsrf=AHTn8zo0lCQ62y9BLQ5CPLYPy1BtigryGw:1743022481173&q=laptop+shop+nearby&rflfq=1&num=10&sa=X&ved=2ahUKEwjhuc3e0KiMAxUzbvUHHY42FIoQjGp6BAgtEAE&biw=1216&bih=940&dpr=1#rlfi=hd:;si:;mv:[[23.8131137,90.4825032],[23.688104499999998,90.3532808]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:10"
    list_of_info = laptop_shop_list(url)
    list_of_info.to_csv("shop_info.csv", index=False)

