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
print(result.status_code)

soup = BeautifulSoup(result.text, 'html.parser')

print(soup.prettify())

