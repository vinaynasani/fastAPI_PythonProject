from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Old version of code to use traditional postgres adaptor for db connection
# import psycopg2

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',
#                                 database='FastApi',
#                                 user='postgres',
#                                 password='09241A0354v!nay',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connection is successful")
#         break
#     except Exception as ex:
#         print("connection to db failed")
#         print("Error: ", ex)
#         time.sleep(2)