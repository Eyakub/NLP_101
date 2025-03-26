from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas as pd
from selenium.common.exceptions import TimeoutException


def scroll_by_height(driver, height):
    for i in range(0, height/2): 
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.1)


def get_product_comments(product_url):
    # options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(product_url)
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#rokomariBody')))
    reviews_data = []
    viewport_height = driver.execute_script("return window.innerHeight")
    print(f"Viewport height: {viewport_height}")

    # Scroll down multiple times to ensure content loads
    total_height = driver.execute_script("return document.body.scrollHeight")
    middle_height = total_height / 4
    driver.execute_script(f"window.scrollTo(0, {middle_height});")

    time.sleep(2)
    while True:
        print("inside while loop...")
        try:
            print("Scraping reviews from page...")
            initial_button = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.text-center.border-y.border-\[\#f1f1f1\].py-4 > button")
            ))
            # Click the button
            driver.execute_script("arguments[0].click();", initial_button)
            print("Clicked show more button...")
            time.sleep(2)
        except TimeoutException:
            print("No more reviews to scrape")
            break

    review_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "singleReview_singleReview__MOGoJ")))
    print(f"Found {len(review_items)} reviews")
    for review in review_items:
        username = review.find_element(By.CSS_SELECTOR, "span.singleReview_name__SBSuW").text
        content = review.find_element(By.CSS_SELECTOR, "div.singleReview_reviewComment__gKQY8 > div > div").text
        reviews_data.append({
            "username": username,
            "content": content
        })
    driver.quit()
    return pd.DataFrame(reviews_data)


if __name__ == "__main__":
    # reviews = get_product_comments("https://www.rokomari.com/book/210878/rasulullah-sm-er-sokal-sondhar-dua-o-zikor-and-doyar-card")
    reviews = get_product_comments("https://www.rokomari.com/book/385692/shaykh-ahmadullah-suggested-2ti-boi")

    reviews.to_csv("rokomari_product_reviews.csv", index=False)
    print(f"Saved {len(reviews)} reviews to daraz_product_reviews.csv")