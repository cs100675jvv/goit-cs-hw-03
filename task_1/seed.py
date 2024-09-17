from faker import Faker
import psycopg2
import random
import traceback

# Конфігурація підключення до бази даних (замінити на реальні параметри при використанні)
db_config = {
    "database": "pgrs_db",
    "host": "localhost",
    "user": "pgrs_user",
    "password": "pgrs_pass",
    "port": "5433"
}

fake = Faker()

def generate_users(n=10):
    """ Генерує випадкові дані для таблиці користувачів """
    users = []
    for _ in range(n):
        user_name = fake.user_name()
        email = fake.email()
        users.append((user_name, email))
    return users


# def generate_statuses():
#     """ Вибирає статус із списка """
#     statuses = ['new', 'in progress', 'completed']
#     for _ in range(len(statuses)):
#         status = random.choice(statuses)
#     return status

def generate_statuses():
    """ Генерує фіксовані статуси для таблиці статусів """
    statuses = [('new',), ('in progress',), ('completed',)]
    return statuses


def generate_tasks(n=30):
    """ Генерує випадкові дані для таблиці завдань """
    tasks = []

    # Отримання id користувачів і статусів
    user_ids = fetch_ids("SELECT id FROM users")
    status_ids = fetch_ids("SELECT id FROM status")

    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.text(max_nb_chars=200)
        status = random.choice(status_ids)
        user_id = random.choice(user_ids)
        tasks.append((title, description, status, user_id))
    return tasks


def fetch_ids(query: str) -> list:
    """ Отримує id із існуючих елементів із бази даних """
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return [row[0] for row in cur.fetchall()]


def populate_database():
    """ Функція для заповнення бази даних """
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Вставка користувачів
        users = generate_users(10)
        cur.executemany("INSERT INTO users (name, email) VALUES (%s, %s)", users)
        conn.commit()

        # Вставка статусів
        # statuses = [(status,) for status in [('new',), ('in progress',), ('completed',)]]
        statuses = generate_statuses()
        cur.executemany("INSERT INTO status (name) VALUES (%s)", statuses)
        conn.commit()

        # Вставка завдань
        tasks = generate_tasks(30)
        cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",tasks)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        traceback.print_exc()
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':

    populate_database()