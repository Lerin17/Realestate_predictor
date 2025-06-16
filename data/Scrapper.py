import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


base_url = "https://propertypro.ng/property-for-sale/in/lagos?page="

# headers = {
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
# (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.google.com",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Connection": "keep-alive"
# }

options = uc.ChromeOptions()
options.add_argument("--headless")  # Optional: remove this line if you want to see the browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")


data = []

for page in range(0, 3):  # Scrape first 5 pages
    print(f"Scraping page {page}...")

    


    if(page == 0):
        url = "https://propertypro.ng/property-for-sale/in/lagos="
    else : 
        url = base_url + str(page)
    
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
         # Use Selenium to get the page source
        # driver.get(url)

        with open(f"page_{page}_dump.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)


        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "property-listing")))


        for _ in range(5):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(1.5)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)

        # time.sleep(7) 
        #  # Wait for the page to load
         # response = requests.get(url, headers=headers)  
    # if response.status_code != 200:
    #     print(f"Failed to retrieve page {page}", response.status_code)
    #     continue

        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print(soup.prettify()[:3000])
        # container = soup.find("div", class_="container") 
        # print("Container found:", container is not None, flush=True)
        # print(container.prettify()[:1000])
        #  # Main container for listings
        listings = soup.find_all("div", class_="property-listing")  # Listing block
        
        print(len(listings), "listings found on page", page, flush=True)
    # ("div", class_="property-info").find("span", class_="price")




        # for listing in listings:
        #     print("Scraping listing... ", flush=True)
        #     try:
        #         title = listing.find("div", class_="pl-title").find("h3").text.strip()              
        #         print(title, 'title', flush=True)
        #         location = listing.find("address").find("p").text.strip()
        #         price = listing.find("div", class_="pl-price").find("h3", class_ ="").text.strip().replace("₦", "").replace(",", "")
        #         bedrooms = listing.find("div", class_="pl-price").find("h6", class_ ="")
        #         # price = listing.find("div", class_="pl-price").text.strip().replace("₦", "").replace(",", "")
        #         # beds = listing.find("ul", class_="listings-property-info").find_all("li")[0].text.strip()


        #         data.append({
        #             "Title": title,
        #             "Location": location,
        #             "Price (NGN)": price,
        #             "Bedrooms": bedrooms
        #         })             
        #         print(f"Total listings scraped: {len(data)}",  flush=True)


        #     except AttributeError:
        #         continue  # Skip listings with missing fields
            
            
            
        
    finally:
            time.sleep(2)  # Be nice to the server

            

            driver.delete_all_cookies()

           
            driver.quit()

        # Convert to DataFrame
            df = pd.DataFrame(data)

# Save to CSV
df.to_csv("data/lagos_properties.csv", index=False)
print("Scraping complete. Data saved to 'data/lagos_properties.csv'")
