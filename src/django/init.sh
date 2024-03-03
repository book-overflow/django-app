cd /app

echo 1

pipenv install

echo 2

pipenv run python manage.py makemigrations

echo 3

pipenv run python manage.py migrate

echo 4

pipenv run python manage.py runserver 0.0.0.0:${BE_PORT}