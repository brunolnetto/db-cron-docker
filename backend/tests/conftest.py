from sqlalchemy import create_engine
from datetime import datetime

from backend.db_cron.database.models import UserDB

def db_client_data():
    data={
        'POSTGRES_DSN_SCHEME': 'postgresql+psycopg2',
        'POSTGRES_USER': 'myuser',
        'POSTGRES_PASSWORD': 'mypassword',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': 5433,  
        'POSTGRES_DBNAME': 'mydb',
    }
    
    return data

def client_uri():
    db_data=db_client_data()
    
    dsn_scheme=db_data['POSTGRES_DSN_SCHEME']
    user=db_data['POSTGRES_USER']
    password=db_data['POSTGRES_PASSWORD']
    host=db_data['POSTGRES_HOST']
    port=db_data['POSTGRES_PORT']
    dbname=db_data['POSTGRES_DBNAME']
    
    return f"{dsn_scheme}://{user}:{password}@{host}:{port}/{dbname}"

def get_test_engine():
    return create_engine(client_uri())

def get_test_users():
    return [
        UserDB(
            id=1,
            username="John Smith",
            email="john@mail.com",
            password="mypwd1234!",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        UserDB(
            id=2,
            username="Amy Johnson",
            email="amy@mail.com",
            password="mypwd1234?",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
    ]

engine=get_test_engine()