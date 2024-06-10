import pytest
import os

from httpx import AsyncClient
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from src.archive.app import app

from src.archive.domains.user import User, Role


@pytest.fixture
async def get_client():
    async with AsyncClient(app=app, base_url="http://test/v1") as client:
        print('\n', 1111111111)
        yield client
        print('\nClient yielded')
    print('\nClient closed')
        


class UserClient:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def login(self, email, password):
        json_data = {"email": email, "password": password}
        response = await self.client.post("/login", json=json_data)
        return response
    
    async def create_document_handler(self, token, files, data):
        headers = {"Authorization": f"Bearer {token}"}
        form_data = {
            "data": data
        }
        response = await self.client.post("/document",files=files, data=form_data, headers=headers)
        return response

    async def close_client(self):
        print("close")
        await self.client.aclose()


@pytest.fixture
async def get_user_client(get_client):
    client = await get_client.__anext__()
    user_client = UserClient(client=client)
    try:
        yield user_client
    finally:
        print(123124)
        await get_client.aclose()
        print(5432)

    # async for client in get_client:
    #     user_client = UserClient(client=client)
    #     return user_client
    # print("123432")


@pytest.fixture(scope="session")
def load_db_url():
    load_dotenv()
    return os.getenv("TEST_POSTGRES_URL")


@pytest.fixture(scope="session")
def init_engine(load_db_url):
    engine = create_async_engine(
        url=load_db_url,
        echo=False
    )

    yield engine

    engine.dispose()


@pytest.fixture
def get_user():
    user = User.create(
        firstname="Firstname",
        lastname="Lastname",
        email="test@email.com",
        password="password",
    )
    return user

@pytest.fixture
def upload_admin_user_to_db(init_engine):
    async def upload(user: User):
        async with init_engine.begin() as conn:
            await conn.execute(
                text("""
                    insert into "user" (
                        firstname,
                        lastname,
                        email,
                        role,
                        hashed_password,
                        created_at
                    ) values (
                        :firstname,
                        :lastname,
                        :email,
                        :role,
                        :hashed_password,
                        :created_at
                    )
                """),
                {
                    "firstname": user.get_firstname,
                    "lastname": user.get_lastname,
                    "email": user.get_email,
                    "role": Role.AdminUser.value,
                    "hashed_password": user.get_password,
                    "created_at": user.get_created_at
                }
            )
    return upload
