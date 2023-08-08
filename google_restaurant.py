import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

db_params = {
    'database': 'mydatabase',
    'user': 'postgres',  # Use the default user
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432',
}

def save_html_response_to_file(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"HTML content saved to file: {file_path}")
        else:
            print(f"Failed to fetch HTML content. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while saving the HTML content to the file: {e}")

def google_search(query):
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    return url

def scrape_google_maps(url):
    # Provide the path to the Chromium/Chrome browser and the compatible WebDriver executable
    chrome_path = '/usr/bin/google-chrome'
    chromedriver_path = '/usr/bin/chromedriver'

    # Setting up the Chromium/Chrome service and options
    chrome_service = ChromeService(executable_path=chromedriver_path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run the browser in headless mode (without GUI)
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode
    chrome_options.add_argument('--window-size=1920x1080')  # Set window size for headless mode

    # Create the headless browser instance
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Scraping logic
    try:
        browser.get(url)

        # Example: Extracting restaurant name and rating
        restaurant_name = browser.find_element(By.CSS_SELECTOR,'h1').text.strip()
        print(restaurant_name)
        restaurant_rating_and_review_number = browser.find_element(By.CLASS_NAME,'F7nice').text.strip()
        print(restaurant_rating_and_review_number)
        browser.save_screenshot('before_click.png')
        more_reviews_button = browser.find_element(By.CSS_SELECTOR, "button.hh2c6[aria-label*='Reviews for']")
        # browser.execute_script("arguments[0].scrollIntoView(true);", more_reviews_button)
        print("Button found:", more_reviews_button)

    # Click the button
        more_reviews_button.click()
        time.sleep(2)
        browser.save_screenshot('after_click.png')

    # Wait for the additional reviews to load (You may need to adjust the wait time as needed)
        # WebDriverWait(browser, 10).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, 'jftiEf'))
        # )
        scrollable_div = browser.execute_script('return document.getElementsByClassName("m6QErb DxyBCb")[0];')
        SCROLL_PAUSE_TIME = 6


# Get scroll height
        last_height = browser.execute_script("return arguments[0].scrollHeight;", scrollable_div)
        print(last_height)
        while True:
            # Scroll down to bottom
            scrollable_div = browser.execute_script('return document.getElementsByClassName("m6QErb DxyBCb")[0];')
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_div)
            browser.save_screenshot("after_height.png")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return arguments[0].scrollHeight;", scrollable_div)
            print(new_height)
            if new_height == last_height:
                break
            last_height = new_height
        print(f"out of loop: {new_height} equal to {last_height}")
        restaurant_elements = browser.find_elements(By.CLASS_NAME,'jftiEf')
        restaurant_reviews = []
        for element in restaurant_elements:
            print("hi")
            button_inside_element = element.find_elements(By.CLASS_NAME, 'w8nwRe')

            # If the button is found, click it
            if button_inside_element:
                print('waiting until the elemnt is clickable')
                WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'w8nwRe'))
                ).click()
                print('is clickable wow sugoi')

            time.sleep(2)
            stars_match = re.search(r'(\d+)\s*star', element.get_attribute('innerHTML'), re.IGNORECASE)
            if stars_match:
                num_stars = int(stars_match.group(1))
                print(f"The restaurant has {num_stars} star(s).")
            else:
                num_stars = "Not found"
                print("Star rating not found.")
            review_text = element.text.strip()
            review_text_with_stars = f"{review_text} (Number of Stars: {num_stars})"
            restaurant_reviews.append(review_text_with_stars)
            print('review added uwu')

        browser.save_screenshot('after_extra.png')
        print(f"Restaurant Name: {restaurant_name}")
        print(f"Rating: {restaurant_rating_and_review_number}")
        print(f"Reviews: {restaurant_reviews}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.quit()  # Close the browser after scraping

if __name__ == "__main__":
    restaurant_name = "Prairie Hills Cafe"
    result = google_search(restaurant_name)
    scrape_google_maps(result)





