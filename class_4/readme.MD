# Web Scraping Tasks

This project includes two web scraping tasks:

1. Get product reviews from Rokomari
2. Get 100 phone numbers from Google about nearby laptop shops

---

## Task 1: Rokomari Product Reviews

**Goal:**  
Scrape user reviews from a product page on [rokomari.com](https://www.rokomari.com).

**Approach:**

- Use Selenium to open the product page.
- Wait for the reviews section to load.
- Extract username and review content.
- Loop through paginated reviews using the "Next" button.
- Stop when no further pages are available.
- Save the data to a CSV file.

---

## Task 2: 100 Phone Numbers of Laptop Shops (Google)

**Goal:**  
Collect up to 100 phone numbers of nearby laptop shops by scraping Google local search results.

**Approach:**

- Use Selenium to open a Google local search URL.
- Loop through search results.
- Extract shop name and phone number from each result.
- Ignore listings without phone numbers.
- Use the "Next" button to paginate through results.
- Stop when 100 valid phone numbers are collected.

**Note:**  
Phone numbers are sometimes embedded with other info (like open hours), so the script uses string parsing or regex to extract only the number.

---
