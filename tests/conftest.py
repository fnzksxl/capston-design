import pytest_asyncio
from httpx import AsyncClient

from app import main, models
from app.database import engine, get_db
from app.config import settings


@pytest_asyncio.fixture(scope="session")
def app():
    if not settings.TESTING:
        raise SystemError("TESTING environment must be set true")

    return main.app


@pytest_asyncio.fixture
async def session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test/api/v1") as ac:
        models.Base.metadata.drop_all(bind=engine)
        models.Base.metadata.create_all(bind=engine)

        yield ac
