import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.indeed.com/jobs?'
site = 'https://www.indeed.com'

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
    pages = pagination.find_all('li')
    for page in pages:
        # print(page.text)
        total_pages.append(page.text)
    # print(total_pages)

    total = int(max(total_pages))
    # print(total)
    return total

def get_all_items():
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

    with open('temp/result.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    soup = BeautifulSoup(res.text, 'html.parser')

    # Scraping process
    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')
    # print(contents.)

    # pick item
    # * title
    # * company name
    # * company link
    # * company address

    job_list = []
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName')
        company_name = company.text
        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link is not available'

        # print(company_link)

        data_dictionary = {
            'title': title,
            'company_name': company_name,
            'link': company_link
        }
        job_list.append(data_dictionary)

    # return job_list
    # cetak data disini
    # print(f" Jumlah data : {len(job_list)}")

    # writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open('json_result/job_list.json', 'w+') as json_data:
        json.dump(job_list, json_data)
    print('json created')

    # create csv
    df = pd.DataFrame(job_list)
    df.to_csv('indeed_data.csv', index=False)
    df.to_excel('indeed_data.xlsx', index=False)

    # data created
    print('Data Created Success')

if __name__ == '__main__':
    # print(get_total_pages())
    get_all_items()