FROM python:3.5.2

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    apt-get install -y nginx supervisor && \
    pip3 install uwsgi

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./ /app

RUN rm -f /app/configuration/local_settings.py

RUN rm /etc/nginx/nginx.conf && \
  ln -s /app/config/nginx/nginx.conf /etc/nginx/ && \
  rm /etc/nginx/sites-enabled/default && \
  ln -s /app/config/nginx/seamstress.conf /etc/nginx/sites-enabled/seamstress.conf && \
  rm /etc/supervisor/supervisord.conf && \
  mkdir -p /app/data/logs && \
  mkdir -p /app/data/media && \
  touch /app/data/logs/logfile.log

RUN python /app/src/manage.py collectstatic --noinput

ENV APP_MODE=web
# APP_MODE web | celery

EXPOSE 80

VOLUME ["/app/data"]

CMD echo "Running with APP_MODE='$APP_MODE'; possible modes: web, celery"; \
    mkdir -p /app/data/logs; \
    mkdir -p /app/data/media; \
    touch /app/data/logs/logfile.log; \
    supervisord -n -c /app/config/supervisord_$APP_MODE.conf


#RUN ln -s /app/config/nginx/seamstress.conf /etc/nginx/sites-enabled/ &&\
#
#    chmod +x /app/django_init.sh
#
#ENTRYPOINT ["/app/django_init.sh"]
#
##ENV DJANGO_ENV=prod
##ENV DOCKER_CONTAINER=1
#
#EXPOSE 8000