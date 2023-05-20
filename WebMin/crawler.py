# Develop a basic crawler for the web search for user defined keywords

import requests
from bs4 import BeautifulSoup

# gets all the links from a given url
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and ':' not in href:
            links.append('https://en.wikipedia.org' + href)
    return links

# searches for a given keyword and returns the top 10 results
def search(keyword):
    url = f'https://en.wikipedia.org/w/index.php?title=Special:Search&limit=10&offset=0&ns0=1&search={keyword}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for result in soup.find_all('div', {'class': 'mw-search-result-heading'}):
        href = result.find('a').get('href')
        if href and href.startswith('/wiki/') and ':' not in href:
            url = 'https://en.wikipedia.org' + href
            results.append(url)
    return results

# crawls the web starting from a given url and up to a given depth
def crawl(start_url, max_depth):
    visited_urls = set()
    urls_to_visit = [(start_url, 0)]
    while urls_to_visit:
        url, depth = urls_to_visit.pop(0)
        if url in visited_urls or depth > max_depth:
            continue
        visited_urls.add(url)
        print(f'Crawling {url}')
        links = get_links(url)
        for link in links:
            urls_to_visit.append((link, depth + 1))

# main function
if __name__ == '__main__':
    keyword = 'python'
    max_depth = 2
    results = search(keyword)
    
    for result in results:
        print(f'Search result: {result}')
        crawl(result, max_depth)
