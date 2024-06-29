import psycopg2
from info_db import db_params



# Подключение к базе данных
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Создание таблицы users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );
''')

# Создание таблицы status
cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );
''')

# Вставка начальных данных в таблицу status
statuses = [('new',), ('in progress',), ('completed',)]
cursor.executemany('''
    INSERT INTO status (name) VALUES (%s)
    ON CONFLICT (name) DO NOTHING;
''', statuses)

# Создание таблицы tasks
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        status_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (status_id) REFERENCES status(id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
''')

# Подтверждение изменений и закрытие подключения
conn.commit()
cursor.close()
conn.close()
