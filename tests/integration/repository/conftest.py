import pytest
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.archive.database.tables import mapper_registry


@pytest.fixture(scope="session")
def load_db_url():
    load_dotenv()
    return os.getenv("TEST_POSTGRES_URL")

@pytest.fixture(scope="session")
def init_engine(load_db_url):
    return create_async_engine(
        url=load_db_url,
        echo=False
    )

@pytest.fixture(scope="session")
def get_session(init_engine):
    session = sessionmaker(
        bind=init_engine, class_=AsyncSession, expire_on_commit=False
    )
    return session()

# @pytest.fixture(scope="module")
# async def setup_database(init_engine):

#     async with init_engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
#         await conn.run_sync(mapper_registry.metadata.create_all)
    
#     yield

#     async with init_engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
    
#     await init_engine.dispose()

