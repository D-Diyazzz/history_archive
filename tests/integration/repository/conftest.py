import pytest
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.archive.database.tables import mapper_registry
from src.archive.domains.document import SearchData


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


@pytest.fixture
def init_search_data():
    return SearchData(
        cypher="cypher",
        fund="fund",
        inventory="inventory",
        case="case",
        leaf="leaf",
        authenticity="authenticity",
        lang="lang",
        playback_method="playback method"
    )

@pytest.fixture
def upload_search_data():
    return SearchData(
        id=1,
        cypher="cypher",
        fund="fund",
        inventory="inventory",
        case="case",
        leaf="leaf",
        authenticity="authenticity",
        lang="lang",
        playback_method="playback method",
        other="other"
    )


# @pytest.fixture(scope="module")
# async def setup_database(init_engine):

#     async with init_engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
#         await conn.run_sync(mapper_registry.metadata.create_all)
    
#     yield

#     async with init_engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
    
#     await init_engine.dispose()

