FROM tiangolo/uwsgi-nginx:python3.8

COPY * /app/
COPY requirements.txt /requirements.txt
COPY ./docker/prestart.sh /app/
COPY ./docker/init-db.py /app/

RUN pip install -r /requirements.txt

ENV NGINX_MAX_UPLOAD 100m
