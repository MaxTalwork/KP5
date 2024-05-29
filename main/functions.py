import requests
import psycopg2


def get_vacancy_data(companies):
    for employer_id in companies:
        params = {'employer_id': employer_id}
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        for vacancy in response.json()['items']:
            vacancy_id = vacancy['id']
            comp_id = vacancy['employer']['id']
            vac_name = vacancy['name']
            try:
                salary = vacancy['salary']['from']
            except TypeError:
                salary = 0
            url = vacancy['url']
            return f'{vacancy_id}, "{vac_name}", {salary}, {comp_id}, "{url}"'


def get_comp_data(companies):
    for employer_id in companies:
        params = {'id': employer_id}
        url_st = f'https://api.hh.ru/employers/{employer_id}'
        response2 = requests.get(url_st, params=params)
        comp_id = int(response2.json()['id'])
        comp_name = response2.json()['name']
        return f'{comp_id}, {comp_name}'


def create_table_vac(host, port, user, password, companies):
    with psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('create table if not exists vacancies(vac_id serial primary key, title varchar(100), '
                           'salary int, comp_id int, url varchar(100))')
            # cursor.execute(f"INSERT INTO vacancies VALUES ({get_vacancy_data(companies)})")
            rows = cursor.fetchall()
            for row in rows:
                print(row)


def create_table_comp(host, port, user, password, companies):
    with psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('create table if not exists companies (comp_id serial primary key, comp_title varchar(100))')
            # cursor.execute(f"INSERT INTO companies VALUES ({get_comp_data(companies)})")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
