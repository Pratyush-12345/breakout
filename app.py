from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def safe_find_element(driver, by, value, timeout=5):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        return None

def scrape_gmb_profile(driver, url):
    try:
        driver.get(url)
        time.sleep(random.uniform(1, 2))

        if "sorry/index" in driver.current_url or "consent.google.com" in driver.current_url:
            logging.warning(f"Redirected to {driver.current_url}. Possible CAPTCHA or consent page.")
            return None

        name = safe_find_element(driver, By.CSS_SELECTOR, 'h1')
        address = safe_find_element(driver, By.CSS_SELECTOR, 'button[data-item-id*="address"]')
        phone = safe_find_element(driver, By.CSS_SELECTOR, 'button[data-item-id*="phone"]')
        hours = safe_find_element(driver, By.CSS_SELECTOR, 'div[aria-label*="Hours"]')
        reviews = safe_find_element(driver, By.CSS_SELECTOR, 'div[aria-label*="reviews"]')
        social_links = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, 'a[data-item-id*="authority"]')]

        data = {
            "Escape Room name": name.text if name else "N/A",
            "Address": address.text if address else "N/A",
            "Phone Number": phone.text if phone else "N/A",
            "URL of escape room": url,
            "Hours of Operation": hours.text if hours else "N/A",
            "Reviews": reviews.text if reviews else "N/A",
            "Links of social media": social_links
        }

        logging.info(f"Successfully scraped data for {url}")
        return data
    except WebDriverException as e:
        logging.error(f"Error scraping {url}: {str(e)}")
        return None

def search_escape_rooms(driver, location, num_results=20):
    try:
        driver.get("https://www.google.com/maps")
        search_box = safe_find_element(driver, By.ID, "searchboxinput")
        if not search_box:
            logging.error("Could not find search box")
            return []

        search_box.send_keys(f"escape rooms in {location}")
        search_box.send_keys(Keys.ENTER)

        urls = []
        attempts = 0
        max_attempts = 10

        while len(urls) < num_results and attempts < max_attempts:
            time.sleep(random.uniform(1, 2))
            
            results = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://www.google.com/maps/place"]')
            
            new_urls = [result.get_attribute('href') for result in results if result.get_attribute('href') not in urls]
            urls.extend(new_urls)
            
            if len(urls) >= num_results:
                break
            
            if results:
                driver.execute_script("arguments[0].scrollIntoView();", results[-1])
            
            attempts += 1

        return urls[:num_results]
    except WebDriverException as e:
        logging.error(f"Error during search: {str(e)}")
        return []

def scrape_city(location, num_results=20):
    driver = create_driver()
    try:
        urls = search_escape_rooms(driver, location, num_results)
        data = []
        for url in urls:
            profile_data = scrape_gmb_profile(driver, url)
            if profile_data:
                data.append(profile_data)
        return data
    finally:
        driver.quit()

def scrape_escape_rooms(cities, total_results=100):
    results_per_city = total_results // len(cities)
    with ThreadPoolExecutor(max_workers=len(cities)) as executor:
        future_to_city = {executor.submit(scrape_city, city, results_per_city): city for city in cities}
        all_data = []
        for future in as_completed(future_to_city):
            city_data = future.result()
            all_data.extend(city_data)
            if len(all_data) >= total_results:
                break
    return all_data[:total_results]

# List of cities to scrape
cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
]

# Run the scraper
scraped_data = scrape_escape_rooms(cities, 100)

# Save data to JSON file
with open('escape_rooms_data_100.json', 'w') as f:
    json.dump(scraped_data, f, indent=2)

logging.info(f"Scraped {len(scraped_data)} escape room profiles and saved to escape_rooms_data_100.json")

# Display the first few entries of the scraped data
print(json.dumps(scraped_data[:5], indent=2))




