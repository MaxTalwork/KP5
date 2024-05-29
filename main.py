from main.functions import create_table_comp, create_table_vac, get_comp_data
from crs.class_db_manager import DBManager

host = '127.0.0.1'
port = '5432'
user = 'postgres'
password = 'Dimtim'

companies = [991318, 2509634, 816, 3735331, 132654, 26250, 89117, 8893, 126025, 2242]

print(get_comp_data(companies))
create_table_vac(host, port, user, password, companies)
create_table_comp(host, port, user, password, companies)

print(DBManager(host, port, user, password).get_companies_and_vacancies_count())
DBManager(host, port, user, password).get_avg_salary()
DBManager(host, port, user, password).get_all_vacancies()
DBManager(host, port, user, password).get_vacancies_with_higher_salary()
DBManager(host, port, user, password).get_vacancies_with_keyword()

