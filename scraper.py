import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def get_prices(search_url: str):
    response = requests.get(search_url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []

    quotes_div = soup.find_all('a', class_='c-kVNwOF')

    for quote in quotes_div:
        product = quote.find('h2', class_='c-ccvUMe')
        product_name = product.get_text(strip=True) if product else None

        price_wrapper = quote.find('span', class_='c-irxNwi')
        inner = price_wrapper.find('span') if price_wrapper else None
        price = inner.get_text(strip=True) if inner else None

        if product_name and price:
            quotes.append({'produto': product_name, 'preco': price})

    return quotes

if __name__ == "__main__":

    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for p in products:
        name = p["name"]
        url = p["url"]
        print(f"\n== {name} ==")
        for q in get_prices(url):
            print(q)