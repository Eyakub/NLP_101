from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Edge()
driver.maximize_window()
driver.set_page_load_timeout(300)

driver.get("https://www.sailor.clothing/category/shirt-gauir")

products = {}

for product_no in range(1, 20):
    PRODUCT_XPATH = f'//*[@id="__next"]/main/section[2]/div[2]/div[2]/div[2]/div/div[{product_no}]'
    product = driver.find_element(By.XPATH, PRODUCT_XPATH)
    link = product.find_element(By.TAG_NAME, "a")
    img = product.find_element(By.TAG_NAME, "img")
    title = product.find_element(By.TAG_NAME, "h4")

    products[product_no] = {
        "title": title.text,
        "link": link.get_attribute("href"),
        "img": img.get_attribute("src")
    }

print(products)

driver.quit()
