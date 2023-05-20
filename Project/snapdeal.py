from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    return f"https://www.snapdeal.com/search?keyword={search_term.replace(' ', '+')}"

def extract_record(item):
    
    title = item.find("p", {"class": "product-title"}).text
    price = item.find("span", {"class": "lfloat product-price"}).text
    discount = item.find("div", {"class": "product-discount"}).find("span").text
    return title, price, discount

def main(search_term):
    driver = webdriver.Chrome()
    driver.get(get_url(search_term))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'class': 'product-desc-rating'})
        
    records = []
    
    for result in results:
        records.append(extract_record(result))

    driver.close()

    return records

if __name__ == '__main__':
    search_term = 'bottle'
    results = main(search_term)
    for result in results:
        print(result)