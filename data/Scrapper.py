import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By

base_url = "https://propertypro.ng/property-for-sale/in/lagos?page="

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

data = []

for page in range(0, 6):  # Scrape first 5 pages
    print(f"Scraping page {page}...")

    if(page == 0):
        url = "https://propertypro.ng/property-for-sale/in/lagos="
    else : 
        url = base_url + str(page)

    response = requests.get(url, headers=headers)
    
   


    if response.status_code != 200:
        print(f"Failed to retrieve page {page}", response.status_code)
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all("div", class_="property-listing")  # Listing block
    
    # ("div", class_="property-info").find("span", class_="price")

    for listing in listings:
        try:
            title = listing.find("div", class_="pl-title").find("h3").text.strip()
            location = listing.find("address").find("p").text.strip()
            price = listing.find("div", class_="pl-price").find("h3", class_ ="").text.strip().replace("₦", "").replace(",", "")
            bedrooms = listing.find("div", class_="pl-price").find()("h6", class_ ="")
            # price = listing.find("div", class_="pl-price").text.strip().replace("₦", "").replace(",", "")
            # beds = listing.find("ul", class_="listings-property-info").find_all("li")[0].text.strip()
        except AttributeError:
            continue  # Skip listings with missing fields
        
        data.append({
            "Title": title,
            "Location": location,
            "Price (NGN)": price,
            "Bedrooms": bedrooms
        })
    
    time.sleep(2)  # Be nice to the server

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("lagos_properties.csv", index=False)

print("Scraping complete. Data saved to 'lagos_properties.csv'")
