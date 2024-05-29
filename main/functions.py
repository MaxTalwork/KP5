import requests
import psycopg2


def get_vacancy_data(employer_id):
    """
    загрузили данные по вакансиям с АПИ ХедХантер
    """
    vac_list = []
    params = {'employer_id': employer_id}
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    for vacancy in response.json()['items']:
        vacancy_id = int(vacancy['id'])
        comp_id = int(vacancy['employer']['id'])
        vac_name = vacancy['name']
        try:
            salary = int(vacancy['salary']['from'])
        except TypeError:
            salary = 0
        url = vacancy['url']
        vac_info = (vacancy_id, vac_name, salary, comp_id, url)
        vac_list.append(vac_info)
        return vac_list


def get_comp_data(employer_id):
    """
    загрузили данные по компаниям с АПИ ХедХантер
    """
    params = {'employer_id': employer_id}
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    for comp in response.json()['items']:
        comp_id = comp['employer']['id']
        comp_name = comp['employer']['name']
        return comp_id, comp_name


def create_table_vac(host, port, user, password, companies):
    """
    создали таблицу вакансий
    """
    with psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('create table if not exists vacancies(vac_id serial primary key, title varchar(100), '
                           'salary int, comp_id int, url varchar(100))')
            for com_id in companies:
                for vacancy in (get_vacancy_data(com_id)):
                    cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s)", vacancy)


def create_table_comp(host, port, user, password, companies):
    """
    создали таблицу компаний
    """
    with psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('create table if not exists companies (comp_id serial primary key, comp_title varchar(100))')
            for comp_data in companies:
                cursor.execute("INSERT INTO companies VALUES (%s, %s)", (get_comp_data(comp_data)))
