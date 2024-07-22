# Используем официальный базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое проекта в контейнер
COPY . .

# Открываем порт 3000 для доступа к приложению
EXPOSE 3000

# Указываем команду для запуска скрипта
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "3000"]
