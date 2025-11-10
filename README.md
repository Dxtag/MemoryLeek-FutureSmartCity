# MemoryLeek-FutureSmartCity
Projekt na hackathon Future Smart City 9.10.2025 - 14.11.2025 
## Uruchomienie 
1. Utwórz plik ze zmiennymi środowiskowymi na podstawie pliku example.env lub skopiuj example.env do pliku .env
2. Z poziomu folderu app uruchom:
   > docker compose up --build -d  
   > docker compose exec gis-server python manage.py migrate  
   > docker compose exec gis-server sh -c 'DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput --username admin --email admin@admin.com'
3. Strona znajduje się na adresie http://localhost:8000
4. Panel administratora znajduę sie na podstronie /admin/
## Data License
Ten projekt zawiera dane z [OpenStreetMap](https://www.openstreetmap.org),
które są dostępne na licencji [Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1-0/).  
This project contains data from [OpenStreetMap](https://www.openstreetmap.org),
which is made available under the [Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1-0/).  
© OpenStreetMap contributors.
