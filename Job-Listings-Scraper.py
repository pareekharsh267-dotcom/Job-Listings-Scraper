import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://quotes.toscrape.com/page/{}/"
data = []
page = 1

while True:
    print(f"Scraping page {page}...")
    url = base_url.format(page)
    
    response = requests.get(url)
    
    if response.status_code != 200:
        break
    
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    
    if not quotes:
        break
    
    for quote in quotes:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        
        data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })
    
    page += 1
    time.sleep(1)

df = pd.DataFrame(data)
df.to_csv("quotes_data.csv", index=False)

print("Scraping completed and data saved!")