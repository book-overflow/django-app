cd /app

echo 1. Installing

pipenv install

pipenv install requests

echo 2. Migrating

pipenv run python manage.py makemigrations

pipenv run python manage.py migrate

echo 3. Creating superuser

pipenv run python manage.py createsuperuser --noinput

echo 4. Setting up

pipenv run python setup.py

echo 5. Running server

pipenv run python manage.py runserver 0.0.0.0:${BE_PORT}