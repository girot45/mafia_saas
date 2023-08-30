FROM python:3.10-slim

# Создание рабочей директории
WORKDIR /mafia_saas

# Копирование списка зависимостей Python
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Запуск приложения
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
