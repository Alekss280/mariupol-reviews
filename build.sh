#!/bin/bash
mkdir -p /root/.cloud-certs && \
python -c "import urllib.request; urllib.request.urlretrieve('https://st.timeweb.com/cloud-static/ca.crt', '/root/.cloud-certs/root.crt')" && \
pip install --upgrade -r requirements.txt && \
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput