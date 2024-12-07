# Базовый образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /backend

# Копируем приложение
COPY . /backend

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт приложения
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]
