#!/bin/bash

# Основной скрипт для сборки образа Docker. Устанавливает зависимости, загружает модель и выполняет миграции.

# Устанавливаем последнюю версию pip

pip install --upgrade pip && \

# Устанавливаем зависимости из файла requirements.txt

pip install -r requirements.txt --noinput && \

# Выполняем миграции и собираем статические файлы для Django

python manage.py migrate --noinput && \

# Собираем статические файлы для Django

python manage.py collectstatic --noinput