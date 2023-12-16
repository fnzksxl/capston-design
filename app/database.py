from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

if not settings.TESTING:
    engine = create_engine(
        "mysql+pymysql://{username}:{password}@{host}:{port}/{name}".format(
            username=settings.DB_USERNAME,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            name=settings.DB_NAME,
        )
    )
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )
else:
    engine = create_engine(
        "mysql+pymysql://{username}:{password}@{host}:{port}/{name}".format(
            username=settings.DB_TEST_USERNAME,
            password=settings.DB_TEST_PASSWORD,
            host=settings.DB_TEST_HOST,
            port=settings.DB_TEST_PORT,
            name=settings.DB_TEST_NAME,
        )
    )
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
