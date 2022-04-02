import os
import requests
from bs4 import BeautifulSoup

url = 'https://www.indeed.com/jobs?'
params = {
    'q': 'Python Developer',
    'l': 'New York State',
    'vjk': '5f2fbaaa634be72b'
}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

result = requests.get(url, params=params, headers=headers)
# print(result.status_code)

soup = BeautifulSoup(result.text, 'html.parser')

def get_total_pages():
    params = {
        'q': 'Python Developer',
        'l': 'New York State',
        'vjk': '5f2fbaaa634be72b'
    }

    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    total_pages = []
    # Scraping Step
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.prettify())
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.findAll('li')
    for page in pages:
        # print(page.text)
        total_pages.append(page.text)
    # print(total_pages)

    total = int(max(total_pages))
    # print(total)
    return total

if __name__ == '__main__':
    print(get_total_pages())