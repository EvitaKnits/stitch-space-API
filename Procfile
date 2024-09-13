release: python manage.py makemigrations && python manage.py migrate
web: gunicorn stitch_space_api.wsgi