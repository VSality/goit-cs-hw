import psycopg2
from info_db import db_params

# Подключение к базе данных
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()


cursor.execute('''
    SELECT * FROM tasks WHERE user_id = 11;
''')
cursor.execute('''
    SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');
''')
cursor.execute('''
    UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 11;
''')
cursor.execute('''
    SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);
''')
cursor.execute('''
    INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('Hello world', 'No more info', (SELECT id FROM status WHERE name = 'new'), 11);
''')
cursor.execute('''
    SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
''')
cursor.execute('''
    DELETE FROM tasks WHERE id = 1;
''')
cursor.execute('''
    SELECT * FROM users WHERE email LIKE 'shawn08@example.com';
''')
cursor.execute('''
    UPDATE users SET fullname = 'Mary' WHERE id = 11;
''')

cursor.execute('''
    SELECT status.name, COUNT(tasks.id) AS task_count
FROM tasks
JOIN status ON tasks.status_id = status.id
GROUP BY status.name;
''')

cursor.execute('''
    SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com';
''')

cursor.execute('''
    SELECT * FROM tasks WHERE description IS NULL OR description = '';
''')

cursor.execute('''
    SELECT users.fullname, tasks.title
FROM users
JOIN tasks ON users.id = tasks.user_id
WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
''')

cursor.execute('''
    SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.fullname;
''')


# Подтверждение изменений и закрытие подключения
conn.commit()
cursor.close()
conn.close()
