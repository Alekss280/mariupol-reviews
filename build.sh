#!/bin/bash

pip install --upgrade -r requirements.txt && \
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput