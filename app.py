import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas

api_data = {}
api_count = 0

url = 'https://www.programmableweb.com/apis/directory'

print(f' ---- SCRAPING STARTED at {datetime.now().time()}')

while True:

    res = requests.get(url)
    data = res.content
    soup = BeautifulSoup(data, 'lxml')


    def odd_even(tag):
        if tag.name == "tr":
            classes = tag.get("class", [])
            return "odd" in classes or "even" in classes


    content = soup.find_all(odd_even)

    for el in content:
        name = el.find('a').text
        url = 'https://www.programmableweb.com' + el.find('a')['href']
        cat_tag = el.find('td', {'class': 'views-field-field-article-primary-category'})
        category = cat_tag.text if cat_tag else 'N/A'
        description = el.find('td', {'class': 'views-field-field-api-description'}).text
        # print('Name:', name, '\nURL:', url, '\nCategory:', category, '\nDescription:', description, '\n-----')
        api_count += 1
        api_data[api_count] = [name, url, category, description]

    base_url = 'https://www.programmableweb.com'
    next_page = soup.find('a', {'title': 'Go to next page'})

    if next_page:
        url = base_url + next_page.get('href')
    else:
        print(f' ---- SCRAPING ENDED at {datetime.now().time()}')
        break

api_data_df = pandas.DataFrame.from_dict(api_data, orient='index', columns=['Name', 'URL', 'Category', 'Description'])
api_data_df.to_csv('api.csv')
print('Total APIs scraped:', api_count)
