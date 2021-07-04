
# migrate db, so we have the latest db schema
cd /code/ && python manage.py migrate

# run server
cd /code/ && python manage.py runserver 0.0.0.0:5000