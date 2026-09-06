# integration Test for the paste Route.

# It gives us a confidence about most things that are involved in the paste retrival process:
# 1. The endpoints, basically the http layer.
# 2. The Paste Service layer, business logic.
# 3. The ORM layer, SQLModel.
# 3. The caching mechanism, Redis.

# It glues everything together ergonomically, thanks to powerful library
# "pytest" and amazing testing capabelities provided by SQLModel and FastAPI

import json
import os

from app.core.cache.cache_interface import Cache
from app.core.cache.cache_redis import RedisCache

os.environ["PASTORE_DEVELOPMENT"] = "True"

from fakeredis import FakeAsyncRedis
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine, select

from app.db import get_cache, get_session
from app.main import app
from app.models.pasted import Pasted, PastedCreate, PastedExpiryDuration, PastedPublic


@pytest.fixture(name="redis_client")
def fakeredis_fixture():
    """Sets up a fakeredis client, an ephemeral/in-memory redis implementation for testing"""
    return FakeAsyncRedis()

# session_fixture yields a session that can be used for other tests.
# Presumably, we're cheating a little bit by using sqlite instead of
# postgresql. But it's better then nothing.
@pytest.fixture(name="session")
def session_fixture():
    """Sets up an sqlmodel session for testing. Also Does the table creation."""

    # Using `StaticPool` will help us maintain a single in-memory database to
    # every test function.
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    # Create the database schema
    SQLModel.metadata.create_all(engine)

    # Add a sample expiry-duration.
    with Session(engine) as session:
        session.add(
            PastedExpiryDuration(
                name="1 day",
                code="oneDay",
                days=1,
            )
        )

        session.commit()

        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session, redis_client: FakeAsyncRedis):
    def get_session_override():
        return session

    def get_cache_override():
        return RedisCache(redis_client)

    # Override the SQLModel's session.
    app.dependency_overrides[get_session] = get_session_override

    # Override the caching dependency func.
    app.dependency_overrides[get_cache] = get_cache_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_pasted_success(client: TestClient):
    """A legitimate paste, must be created successfully"""

    content = "lorem ipsum dolor"

    # 1. Create
    response = client.post(
        "/pastes", json={"content": content,"expiry_code": "oneDay","is_one_time": False}
    )

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["content"] == content

    # 2. Now, fetch the result.
    shortcode = data["shortcode"]
    response = client.get(f"/pastes/?shortcode={shortcode}")

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["content"] == content


def test_create_paste_failure(client: TestClient):
    ## Should endup with Bad Request error, because of the non-existent expiry_code.
    response = client.post(
        "/pastes",
        json={
            "content": "lorem ipsum dolor",
            "expiry_code": "yas",
            "is_one_time": False
        },  # duration value is invalid.
    )

    # assert response.status_code != 200
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_pasted_one_time(client: TestClient):
    """A one time paste shouldn't be available on the second read attempts"""

    content = "lorem ipsum dolor"

    # 1. Create
    response = client.post(
        "/pastes", json={"content": content,"expiry_code": "oneDay","is_one_time": True}
    )

    data = response.json()

    # 2. Now, fetch the result.
    shortcode = data["shortcode"]
    response = client.get(f"/pastes/?shortcode={shortcode}")

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["content"] == content


    # 3. Second attempt

    response = client.get(f"/pastes/?shortcode={shortcode}")

    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_view_count_logic(client: TestClient, session: Session):
    """View count of the paste should increment"""
    # 1. Create
    response = client.post("/pastes", json={"content": "rabio", "expiry_code": "oneDay","is_one_time": False})

    data = response.json()

    assert response.status_code == 201
    assert data["content"] == "rabio"

    shortcode = data["shortcode"]

    response = client.get(f"/pastes/?shortcode={shortcode}")

    statement = select(Pasted).where(Pasted.shortcode == shortcode)
    pasted_item = session.exec(statement).first()

    assert pasted_item
    assert pasted_item.view_count == 1

async def test_paste_redis_hitness(client: TestClient, redis_client: FakeAsyncRedis):
    """The cache should hit, without looking up to the SQL database"""

    # Phase 1: Manually putting cache record and let the application to load
    # Defining an non-existent Paste and putting it into the cache.

    paste_item = PastedPublic(content="Whoah. Pytest is cool",shortcode="2nsj32")

    await redis_client.set(
        name=f"paste_code:{paste_item.shortcode}",
        value=paste_item.model_dump_json()
    )


    response = client.get(f"/pastes/?shortcode={paste_item.shortcode}")

    
    assert response.status_code == 200

    data = response.json()

    assert data['shortcode'] == paste_item.shortcode

    # Phase 2: Posting a paste, then getting it, and then, check to see if the cache is populated or not.
    # Defining an non-existent Paste and putting it into the cache.
    
    paste_item = PastedCreate(
        content="Whoah. Pytest is cool",
        expiry_code="oneDay",
        is_one_time=False
    )

    response = client.post("/pastes", json=paste_item.model_dump() )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    shortcode = data['shortcode']
    get_response = client.get(f"/pastes/?shortcode={shortcode}")

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == data

    stored = await redis_client.get(f"paste_code:{shortcode}")

    assert stored

    assert json.loads(stored) == data
    
