import time
import random
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


#----------------------------------- ANTI BOT SETTINGS ------------------------------------

def get_driver():

    chrome_options = Options()

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver



#----------------------------------- SCROLL FUNCTION -----------------------------------

def scroll_page(driver, scrolls=20):

    for i in range(scrolls):

        print(f"Scrolling {i+1}")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(random.uniform(2,4))

        try:
            load_more = driver.find_element(By.XPATH, '//button//span[text()="50 more"]')
            load_more.click()
            print("Clicked Load More")

            time.sleep(random.uniform(3,5))

        except:
            print("No Load More Button")
            break



#----------------------------------- EXTRACT MOVIE LINKS -----------------------------------

def extract_links(driver):

    movies = driver.find_elements(By.XPATH, '//a[contains(@href, "/title/")]')

    links = []

    for m in movies:
        link = m.get_attribute("href")

        if "/title/" in link and "ref_" in link:
            clean = link.split("?")[0]
            links.append(clean)

    links = list(set(links))

    return links



#----------------------------------- MAIN SCRAPER -----------------------------------

def main():

    driver = get_driver()

    url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2025-01-01,2026-12-31&num_votes=1000,&sort=year,asc"

    driver.get(url)

    time.sleep(5)

    scroll_page(driver, scrolls=25)

    links = extract_links(driver)

    df = pd.DataFrame({"movie_url": links})
    df['Scrape_Category'] = 'New Movies'

    df.to_csv("raw_data/New_Movies.csv", index=False)

    print(f"Total Movies Collected: {len(links)}")

    driver.quit()


if __name__ == "__main__":
    main()