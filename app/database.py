# import psycopg2
# import os


# def get_database_connection():
#     return psycopg2.connect(
#         dbname=os.environ["PGDATABASE"],
#         user=os.environ["PGUSER"],
#         password=os.environ["PGPASSWORD"],
#         host=os.environ["PGHOST"],
#         port=os.environ["PGPORT"],
#     )



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ["PGUSER"]}:{os.environ["PGPASSWORD"]}@{os.environ["PGHOST"]}/{os.environ["PGDATABASE"]}'
SQLALCHEMY_DATABASE_URL = os.environ["PGURL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()