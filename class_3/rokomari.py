import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


base_url = "https://www.rokomari.com/book/category/90/engineering"


def scrap_rokomari(base_url):
    driver = webdriver.Edge()
    driver.maximize_window()
    # driver.set_page_load_timeout(300)

    driver.get(base_url)
    wait = WebDriverWait(driver, 10)

    def get_total_items(driver):
        no_items_xpath = '/html/body/div[8]/div/div/div/section[2]/div[1]/div/div/p'
        no_items = driver.find_element(By.XPATH, no_items_xpath)
        total_items = int(re.search(r'of (\d+) items', no_items.text).group(1))
        return total_items

    def get_total_pages():
        pagination_div = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='pagination']")))

        page_links = pagination_div.find_elements(By.TAG_NAME, "a")
        page_numbers = [int(link.text) for link in page_links if link.text.isdigit()]
        return max(page_numbers)

    total_pages_r = get_total_pages()
    all_product_data = []

    for page_number in range(1, total_pages_r + 1):
        page_url = f"{base_url}?page={page_number}"
        driver.get(page_url)
        try:
            books = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "books-wrapper")))
            book_items = books.find_elements(By.CLASS_NAME, "books-wrapper__item")
            for book in book_items:
                try:
                    rating_section = book.find_element(By.CLASS_NAME, "rating-section")
                    rating_count = rating_section.find_element(By.XPATH, ".//span[@class='text-secondary']").text
                except Exception as e:
                    rating_count = "N/A"

                books_data = {
                    "title": book.find_element(By.TAG_NAME, 'a').get_attribute('title'),
                    "link": book.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                    "author": book.find_element(By.CLASS_NAME, 'book-author').text,
                    "rating": rating_count,
                    }
                all_product_data.append(books_data)
        except Exception as e:
            print(f"Error scraping page {page_number}: {e}")
    print(all_product_data)
    driver.quit()
    return all_product_data


product_data = scrap_rokomari(base_url)
df = pd.DataFrame(product_data)
df.to_csv('product_data.csv', index=False)
print("=====Data saved to product_data.csv=====")
