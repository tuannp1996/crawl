from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pymongo

# Set up MongoDB connection
client = pymongo.MongoClient("mongodb://10.8.0.1:27017/")
db = client["home"]  # Database name
collection = db["house"] 

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--enable-unsafe-swiftshader')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.get("https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi/gia-tu-2-ty-den-3-ty")

time.sleep(5)  # Wait for JS-rendered content

def scrape_page():

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.select("a.js__product-link-for-product-id")

    print(f"Found {len(cards)} listing(s).\n")

    for card in cards:
        #print(f"🏠 card: {card}")
        if card:
            listing_data = {}
            # Extract the data-product-id and title
            product_id = card.get("data-product-id", "No product ID")
            title = card.get("title", "No title")
            
            # Extract the link
            href = card.get("href", "#")
            full_link = f"https://batdongsan.com.vn{href}"

            # Extract image URL
            img_tag = card.select_one("div.re__card-image img.lazyload")
            image_url = ''
            if img_tag:
                image_url = img_tag.get("data-src", "No image URL")

            print(f"Product ID: {product_id}")
            print(f"Title: {title}")
            print(f"Link: {full_link}")
            print(f"Main image: {image_url}")

            listing_data["product_id"] = product_id
            listing_data["title"] = title
            listing_data["link"] = full_link
            listing_data["image_url"] = image_url

                # Extract Price
            price = card.select_one("span.re__card-config-price.js__card-config-item")
            price = price.get_text(strip=True) if price else "No price"
            
            # Extract the area
            area = card.select_one("span.re__card-config-area.js__card-config-item")
            area = area.get_text(strip=True) if area else "No area"

            # Extract price per square meter
            price_per_m2 = card.select_one("span.re__card-config-price_per_m2.js__card-config-item")
            price_per_m2 = price_per_m2.get_text(strip=True) if price_per_m2 else "No price per m²"

            # Extract the number of bedrooms
            bedrooms = card.select_one("span.re__card-config-bedroom.js__card-config-item")
            bedrooms = bedrooms.get_text(strip=True) if bedrooms else "No bedroom info"

            # Extract the location
            location = card.select_one("div.re__card-location span")
            location = location.get_text(strip=True) if location else "No location"

            listing_data["price"] = price
            listing_data["titareale"] = area
            listing_data["price_per_m2"] = price_per_m2
            listing_data["bedrooms"] = bedrooms
            listing_data["location"] = location

            # Store the listing in MongoDB
            collection.insert_one(listing_data)
    print(f"Scraped and saved {len(cards)} listings.")

# Function to go to the next page
def go_to_next_page():
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".re__pagination-next a")
        if next_button:
            next_button.click()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error going to next page: {e}")
        return False

# Scrape multiple pages
page_num = 1
while True:
    print(f"Scraping page {page_num}...")
    scrape_page()

    # Try to go to the next page
    if not go_to_next_page():
        print("No more pages or error going to the next page. Stopping.")
        break

    # Wait for the next page to load
    time.sleep(5)

    page_num += 1

# Close the driver
driver.quit()