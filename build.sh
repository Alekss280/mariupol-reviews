#!/bin/bash
mkdir -p ~/.cloud-certs && \
curl -o ~/.cloud-certs/root.crt "https://st.timeweb.com/cloud-static/ca.crt" && \
chmod 0600 ~/.cloud-certs/root.crt && \
pip install --upgrade -r requirements.txt && \
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput