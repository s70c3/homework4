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

# Команда для запуска Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5123", "app:app"]