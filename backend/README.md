#Flask backend to provide a simple API

##Dependencies
    pip install -r requirements.txt

##Migrations
    alembic upgrade head

##Server
    gunicorn backend.api:app
