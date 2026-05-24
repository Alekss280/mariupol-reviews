#!/bin/bash

# Основной скрипт для сборки образа. Устанавливает зависимости, загружает модель и выполняет миграции.

# Устанавливаем зависимости из requirements.txt

pip install --upgrade -r requirements.txt && \

# Выполняем миграции для Django

python manage.py migrate --noinput && \

# Собираем статические файлы для Django

python manage.py collectstatic --noinput