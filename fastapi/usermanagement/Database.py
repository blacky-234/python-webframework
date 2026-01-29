from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

db_url = 'sqlite:///test.db'
engine = create_engine(db_url, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()



def init_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()