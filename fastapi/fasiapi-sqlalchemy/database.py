from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from contextlib import contextmanager


from urllib.parse import quote_plus

db_passwd = quote_plus("djangomypassword")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://djangouser:{db_passwd}@172.21.0.3:5432/fastpialchemy"
SQLALCHEMY_DATABASE_URL_FASTAPI = f"postgresql+asyncpg://djangouser:{db_passwd}@172.21.0.3:5432/fastpialchemy"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL_FASTAPI, pool_pre_ping=True,echo=True)
SessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False,autocommit=False,autoflush=False)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except:
            await db.rollback()
            raise
        finally:
            await db.close()

