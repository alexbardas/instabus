#Flask backend to provide a simple API

##Dependencies
    pip install -r requirements.txt

##Migrations
    alembic upgrade head

##Server (from project root)
    gunicorn api:app