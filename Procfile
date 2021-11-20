web: gunicorn --pythonpath companies companies.wsgi
release: python companies/manage.py makemigrations
release: python companies/manage.py migrate