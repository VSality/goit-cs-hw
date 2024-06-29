import psycopg2
from faker import Faker
import random
from info_db import db_params

# Подключение к базе данных
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Инициализация Faker
fake = Faker()

# Вставка данных в таблицу users
def insert_users(num_users):
    users = []
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        users.append((fullname, email))

    cursor.executemany('''
        INSERT INTO users (fullname, email) VALUES (%s, %s);
    ''', users)

# Вставка данных в таблицу status
def insert_status():
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany('''
        INSERT INTO status (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    ''', statuses)

# Вставка данных в таблицу tasks
def insert_tasks(num_tasks):
    cursor.execute('SELECT id FROM status')
    status_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]

    tasks = []
    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        tasks.append((title, description, status_id, user_id))

    cursor.executemany('''
        INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
    ''', tasks)

# Вызов функций для вставки данных
insert_users(10)
insert_tasks(20)

# Подтверждение изменений и закрытие подключения
conn.commit()
cursor.close()
conn.close()
