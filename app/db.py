from fastapi import Request
from sqlmodel import SQLModel, Session, create_engine, text
from sqlalchemy.engine import URL
from app.core import config, logs
import redis.asyncio as redis

from app.core.cache.cache_interface import Cache

url_object = URL.create(
    "postgresql+psycopg",
    config.settings.Database_Username,
    config.settings.Database_Password,
    config.settings.Database_Host,
    config.settings.Database_Port,
    config.settings.Database_Name,
)

engine = create_engine(url_object)

def create_db_and_tables():
    """Should not be used in production environment"""
    SQLModel.metadata.create_all(engine)

def test_engine_connectivity():
    logger = logs.get_logger()
    try: 
        conn = engine.connect()
        _ = conn.execute(text('SELECT 1'))
        logger.info('✅ Successfully connceted to database!')
    except Exception as e:
        logger.info('\n\n ❗️ Connection to database failed!')
        raise e    


def get_session():
    """Yields a single session to the underlying database connection"""
    with Session(engine) as session:
        yield session



async def get_redis_client():
    """Returns the client"""
    if config.settings.Redis_Enabled:
        client = redis.Redis(
            host=config.settings.Redis_Host,
            port=config.settings.Redis_Port,
            password=config.settings.Redis_Password,
            decode_responses=True
        )

        return client


    return None

def get_cache(request: Request) -> Cache:
    """Returns an the global redis_client instance."""
    return request.app.state.cache
