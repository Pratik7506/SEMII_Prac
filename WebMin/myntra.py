from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    return f"https://www.myntra.com/{search_term.replace(' ', '+')}"

def extract_record(item):
    try:    
        brand = item.find("h3", {"class": "product-brand"}).text
        title = item.find("h4", {"class": "product-product"}).text
        price = item.find("span", {"class": "product-discountedPrice"}).text
        discount = item.find("span", {"class":"product-discountPercentage"}).text
        return title, brand, price, discount
    except:
        return "", "", "", ""    

def main(search_term):
    driver = webdriver.Chrome()
    driver.get(get_url(search_term))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('li', {'class': 'product-base'})
        
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