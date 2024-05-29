import psycopg2


class DBManager:

    def __init__(self, host, port, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password)

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        """
        query = 'SELECT comp_title, COUNT(vac_id) FROM companies INNER JOIN vacancies USING (comp_id) GROUP BY comp_title'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return f'азвание компании и кол-во вакансий: {cursor.fetchall()}\n'

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = 'select * from vacancies INNER JOIN companies USING (comp_id)'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return (f'список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на '
                    f'вакансию: {cursor.fetchall()}\n')

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        """
        query = 'select avg(salary) from vacancies'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return f'средняя зарплата по вакансиям: {cursor.fetchall()}\n'

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = 'select * from vacancies where salary > (select avg(salary) from vacancies)'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return f'список всех вакансий, у которых зарплата выше средней по всем вакансиям: {cursor.fetchall()}\n'

    def get_vacancies_with_keyword(self):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        user_req = input('Введите ваш запрос: ').lower()
        query = f"select * from vacancies where lower(title) like '%{user_req}%'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tab):
        self.connection.close()
