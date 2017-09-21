FROM python:3.5.2

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    pip3 install uwsgi

COPY . /app

RUN pip3 install -r /app/requirements.txt
RUN chmod +x /app/django_init.sh

ENTRYPOINT ["/app/django_init.sh"]

#ENV DJANGO_ENV=prod
#ENV DOCKER_CONTAINER=1

EXPOSE 8000