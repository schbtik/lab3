
# FROM python:3.10-slim

# WORKDIR /app

# COPY . /app/

# RUN pip install -r requirements.txt

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.10-slim

WORKDIR /app

COPY . /app/

# Устанавливаем зависимости напрямую — без виртуального окружения
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

