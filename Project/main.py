from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    base_url = "https://www.amazon.in/s?k={}&rh=n%3A1389401031&ref=nb_sb_noss"
    search_term = search_term.replace(' ', '+')
    return base_url.format(search_term)

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.in/" + atag.get('href')   
    try:
        price = item.find('span', {'class': 'a-price'}).find('span', {'class': 'a-offscreen'}).text
    except AttributeError:
        return
    try:
        rating = item.i.text
    except AttributeError:
        rating = ''
    return (description, price, rating, url)

def main(search_term):
    driver = webdriver.Chrome()
    driver.get(get_url(search_term))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    records = []
    for item in results:
        record = extract_record(item)
        if record:
            records.append(record)
    driver.close()
    return records

if __name__ == '__main__':
    search_term = 'shoes'
    results = main(search_term)
    for result in results:
        print(result)