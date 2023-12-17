import bcrypt
import pytest_asyncio
import json
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
    async with AsyncClient(app=app, base_url="http://test/v2") as ac:
        models.Base.metadata.drop_all(bind=engine)
        models.Base.metadata.create_all(bind=engine)

        yield ac


@pytest_asyncio.fixture
def user(session) -> models.User:
    salt_value = bcrypt.gensalt()
    pw = bcrypt.hashpw("testpw".encode(), salt_value)
    row = models.User(password=pw, email="test@sample.com")
    session.add(row)
    session.commit()

    return row


@pytest_asyncio.fixture
def item(session, user) -> models.TsItem:
    row = models.TsItem(
        dialect="dialect",
        standard="standard",
        english="english",
        chinese="chinese",
        japanese="japanese",
        owner_id=user.id,
    )
    session.add(row)
    session.commit()

    return row


@pytest_asyncio.fixture
def guestbook(session, user) -> models.GuestBook:
    row = models.GuestBook(message="test", message_owner="test_owner", owner_id=user.id)
    session.add(row)
    session.commit()

    return row


@pytest_asyncio.fixture
async def token(client, user) -> str:
    body = {"email": user.email, "password": "testpw"}
    r = await client.post("/users/login", data=json.dumps(body))

    return r.headers.get("access_token")
