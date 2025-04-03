import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.logger import log

BASE_URL = "https://world.openfoodfacts.org/category/alcoholic-beverages"
OUT_DIR = f"output/{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

os.makedirs(f"{OUT_DIR}/images", exist_ok=True)

def scrape_products():
    response = requests.get(BASE_URL + ".json", headers=HEADERS)
    if response.status_code != 200:
        log(f"Failed to fetch data: {response.status_code}")
        return

    data = response.json()
    products = []

    for product in data.get("products", []):
        name = product.get("product_name", "unknown").strip()
        upc = product.get("code", "unknown")
        img_url = product.get("image_url")

        if not upc or not img_url:
            continue

        try:
            img_resp = requests.get(img_url, headers=HEADERS)
            img_path = f"{OUT_DIR}/images/{upc}.jpg"
            with open(img_path, "wb") as img_file:
                img_file.write(img_resp.content)
        except Exception as e:
            log(f"Error downloading image for {upc}: {e}")
            continue

        products.append([upc, name, img_url])

    csv_path = f"{OUT_DIR}/products.csv"
    with open(csv_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["UPC", "Name", "Image URL"])
        writer.writerows(products)

    log(f"Scraped {len(products)} products to {csv_path}")

if __name__ == "__main__":
    scrape_products()
