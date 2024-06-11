#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
#python manage.py migrate --fake default
python manage.py migrate
python manage.py migrate django_cron
python manage.py loaddata /opt/MedItCRM/main.json
python manage.py loaddata /opt/MedItCRM/ecp.settings.json
#rm /opt/MedItCRM/main.json /opt/MedItCRM/ecp.settings.json

service cron start
exec "$@"