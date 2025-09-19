# QuickWeb_BE

Steps for start project:

make run

or

1 cd quick_web
2 start venv fo python - source .venv/bin/activate
3 cd ..
4 start Django server - python manage.py runserver

For add new element in model : python manage.py makemigrations
python manage.py migrate

changed pull - git pull origin main

conect AWS server
ssh -i /Users/sergeipetuhov/Downloads/myproject.pem ubuntu@13.61.13.177

cd ~/QuickWeb_BE
source venv/bin/activate
gunicorn quick_web.wsgi:application --bind 0.0.0.0:8000
