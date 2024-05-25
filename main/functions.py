import requests
import psycopg2


companies = [991318, 2509634, 816, 3735331, 132654, 26250, 89117, 8893, 126025, 2242]

for employer_id in companies:
    params = {'employer_id': employer_id}
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    for vacancy in response.json()['items']:
        print(vacancy['name'])
    url_st = f'https://api.hh.ru/employers/{employer_id}'
    response2 = requests.get(url_st, params=params)
    print(f'\nComp')
    print(f'{response2.json()['name']}\n')
