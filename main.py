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

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

result = requests.get(url, params=params, headers=headers)
# print(result.status_code)

soup = BeautifulSoup(result.text, 'html.parser')


def get_total_pages(query, location):
    parameters = {
        'q': query,
        'l': location,
        'vjk': '5f2fbaaa634be72b'
    }

    res = requests.get(url, params=parameters, headers=headers)

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
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)

    total = int(max(total_pages))
    # print(total)
    return total


def get_all_items(query, location, start, page):
    parameters = {
        'q': query,
        'l': location,
        'start': start,
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

    with open(f"json_result/{query}_in_{location}_page_{page}.json", 'w+') as json_data:
        json.dump(job_list, json_data)
    print('json created')

    return job_list


def create_document(dataFrame, fileName):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_result/{fileName}.csv', index=False)
    df.to_excel(f'data_results{fileName}.xlsx', index=False)

    print(f'File {fileName}.csv and {fileName}.xlsx successfully created')


def run():
    query = input('Enter Your Query: ')
    location = input('Enter Your Location: ')
    total = get_total_pages(query, location)
    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_all_items(query, location, counter, page)

    # formatting data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data JSON Created')

    # create document
    create_document(final_result, query)


if __name__ == '__main__':
    run()
