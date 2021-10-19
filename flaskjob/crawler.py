"""
Created on Fri Aug 20 16:40:45 2021

@author: wangweizheng
"""

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_url(position, location):
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url


def get_record(card):
    atag = card.a
    job_title = card.find_all('span')[1].text.strip()
    job_url = 'https://www.indeed.com' + atag.get('href')
    company = card.find('span', 'companyName').text.strip()
    job_location = card.find('div', 'companyLocation').get('data-rc-loc')
    job_summary = card.find('div', 'job-snippet').text.strip()
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        job_salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        job_salary = ''
    record = (job_title, company, job_location, post_date, today, job_summary, job_salary, job_url)
    return record


def main(position, location):
    records = []
    url = get_url(position, location)
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'slider_container')

        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary', 'JobUrl'])
        writer.writerows(records)


main('senior accountant', 'new york')