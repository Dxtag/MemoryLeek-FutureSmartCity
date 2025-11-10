docker compose up --build -d
docker compose exec gis-server python manage.py migrate
docker compose exec gis-server sh -c 'DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput --username admin --email admin@admin.com'
