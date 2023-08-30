#!/bin/bash

#Используйте этот файл, при старте работы с "пустым" проектом

echo "Создание миграций"
python3 manage.py makemigrations
echo "Применение миграций"
python3 manage.py migrate
echo "Создайте суперпользователя"
python3 manage.py createsuperuser