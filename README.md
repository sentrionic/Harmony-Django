# Harmony-Django

Harmony is an [Instagram](https://www.instagram.com/) like website using Django.

## Features

- Story CRUD
- Following System
- Search by username or hashtags
- Like system
- An (incomplete) [Android app](https://github.com/sentrionic/HarmonyApp) that communicates with the REST endpoints.

## Stack

- [Django](https://www.djangoproject.com/) for the backend and the templating engine.
- [Django REST framework](https://www.django-rest-framework.org/) for the REST backends
- PostgreSQL
- S3 for storing files
- [Bootstrap](https://getbootstrap.com/) for styling

## Installation

0. Install Python 3.7.3
1. Clone this repository
2. Create a virtual environment
3. Run `pip install -r requirements.txt` to install all the dependencies
4. Add the required values to `settings.py`:
   - Database
   - S3
   - Gmail
5. Run `python manage.py collectstatic && python manage.py makemigrations && python manage.py migrate`.
6. Run `python manage.py runserver`.
7. Go to `localhost:8080`.

## Credits

- [codingwithmitch](https://codingwithmitch.com/courses/building-a-website-django-python/): This project is based on his Django Blog course.
