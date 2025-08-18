import requests
from bs4 import BeautifulSoup

gopro_price_url = "https://www.kuantokusta.pt/search?q=Action%20Cam%20Gopro%20Hero%2012%20Black"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response = requests.get(gopro_price_url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

quotes = []

quotes_div = soup.find_all('a', class_='c-kVNwOF')
# print(quotes_div)

for quote in quotes_div:

    product = quote.find('h2', class_='c-ccvUMe')
    product_name = product.get_text(strip=True) if product else None

    price_wrapper = quote.find('span', class_='c-irxNwi')
    price = price_wrapper.find('span').get_text(strip=True) if price_wrapper else None

    quotes.append({
        'produto': product_name,
        'preço': price
    })

for q in quotes:
    print(q)