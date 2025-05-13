from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--enable-unsafe-swiftshader')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.get("https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi/gia-tu-2-ty-den-3-ty")

time.sleep(5)  # Wait for JS-rendered content

soup = BeautifulSoup(driver.page_source, 'html.parser')

cards = soup.select("a.js__product-link-for-product-id")

print(f"Found {len(cards)} listing(s).\n")

for card in cards:
    #print(f"🏠 card: {card}")
    if card:
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

        # Print the extracted details
        print(f"💰 Price: {price}")
        print(f"📏 Area: {area}")
        print(f"💲 Price per m²: {price_per_m2}")
        print(f"🛏 Bedrooms: {bedrooms}")
        print(f"📍 Location: {location}")
        print("-" * 60)
    # # Find the anchor tag with the product link
    # link_tag = card.select_one("a.js__product-link-for-product-id")
    

    # # Extract the title from the correct div
    # title_tag = link_tag.select_one(".pr-title js__card-title") if link_tag else None

    # title = title_tag.get_text(strip=True) if title_tag else "No title"
    
    # # Extract the href for the full link
    # href = link_tag['href'] if link_tag and link_tag.has_attr('href') else "#"
    # full_link = f"https://batdongsan.com.vn{href}"

    # # Get price (if available)
    # price = card.select_one(".re__card-config-price").get_text(strip=True) if card.select_one(".re__card-config-price") else "N/A"

    # # Get location/address
    # address = card.select_one(".re__card-config-location").get_text(strip=True) if card.select_one(".re__card-config-location") else "N/A"

    # # Print the extracted information
    # print(f"🏠 Title: {title}")
    # print(f"🔗 Link: {full_link}")
    # print(f"💰 Price: {price}")
    # print(f"📍 Address: {address}")
    # print("-" * 60)

driver.quit()