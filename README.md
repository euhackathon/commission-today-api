commission-today
================

Discover the agenda of the EU Commissioners.

## Setup

1. `cd backend`
2. `pip install -r requirements.txt`
3. `python manage.py syncdb`
3. `python manage.py createdata`
4. `python manage.py runserver`
5. Visit the [entry point](http://localhost:8000/api/v1/?format=json)
6. Create an admin account by running `python manage.py createsuperuser`
7. Go to the [admin panel](http://localhost:8000/admin/) and have fun
8. `python manage.py scrape`
8. `python manage.py rebuildindex`
