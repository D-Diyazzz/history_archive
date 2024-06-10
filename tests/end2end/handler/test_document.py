import pytest
import json
import os
from io import BytesIO
from src.archive.database.tables import mapper_registry


@pytest.fixture
def get_document_dict():
    data = json.dumps({
        "author": "author",
        "dating": "2020",
        "place_of_creating": "almaty",
        "variety": "variety",
        "addressee": "addressee",
        "brief_content": "brief content",
        "case_prod_number": "case prod number",
        "main_text": "main text",
        "search_data": {
            "cypher": "cypher",
            "fund": "fund",
            "inventory": "inventory",
            "case": "case",
            "leaf": "leaf",
            "authenticity": "authenticity",
            "lang": "lang",
            "playback_method": "playback method"
        }
    })
    return data


@pytest.mark.asyncio
async def test_create_document_handler(
    init_engine,
    get_user_client, 
    get_user, 
    upload_admin_user_to_db,
    get_document_dict
):
    engine = init_engine
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    user = get_user
    await upload_admin_user_to_db(user)

    gen_client = get_user_client
    client = await anext(gen_client)
    response = await client.login(email="test@email.com", password="password")
    access_token = response.json()["access_token"]

    file_url = 'file_1.pdf'

    files = [
        ("files", ('file_1.pdf', b"file data", 'application/pdf'))
    ]
    
    response = await client.create_document_handler(
        token=access_token,
        files=files,
        data=get_document_dict
    )
    response_data = response.json()
    assert response_data["id"] == 1
    assert file_url in response_data["file_urls"][0]
    assert response_data["author"] == "author"
    assert response_data["dating"] == "2020"
    assert response_data["place_of_creating"] == "almaty"
    assert response_data["variety"] == "variety"
    assert response_data["addressee"] == "addressee"
    assert response_data["brief_content"] == "brief content"
    assert response_data["case_prod_number"] == "case prod number"
    assert response_data["main_text"] == "main text"

    search_data = response_data["search_data"]
    assert search_data["cypher"] == "cypher"
    assert search_data["fund"] == "fund"
    assert search_data["inventory"] == "inventory"
    assert search_data["case"] == "case"
    assert search_data["leaf"] == "leaf"
    assert search_data["authenticity"] == "authenticity"
    assert search_data["lang"] == "lang"
    assert search_data["playback_method"] == "playback method"

    with open(f"files/{response_data['file_urls'][0]}", "rb") as f:
        file_content = f.read()
        assert file_content == b"file data"

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
    
    await engine.dispose()
    await get_user_client.aclose()
    os.remove(f"files/{response_data['file_urls'][0]}")


@pytest.mark.asyncio
async def test_create_with_two_files_document_handler(
    init_engine,
    get_user_client, 
    get_user, 
    upload_admin_user_to_db,
    get_document_dict
):
    engine = init_engine
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    user = get_user
    await upload_admin_user_to_db(user)

    gen_client = get_user_client
    client = await anext(gen_client)

    response = await client.login(email="test@email.com", password="password")
    print(response)
    access_token = response.json()["access_token"]
    
    file_url = 'file_1.pdf'
    file_url_2 = 'file_2.png'

    files = [
        ("files", (file_url, b"file data", 'application/pdf')),
        ("files", (file_url_2, b"file data", 'image/png'))
    ]

    response = await client.create_document_handler(
        token=access_token,
        files=files,
        data=get_document_dict
    )

    response_data = response.json()
    assert response_data["id"] == 1
    assert file_url in response_data["file_urls"][0]
    assert file_url_2 in response_data["file_urls"][1]
    assert response_data["author"] == "author"
    assert response_data["dating"] == "2020"
    assert response_data["place_of_creating"] == "almaty"
    assert response_data["variety"] == "variety"
    assert response_data["addressee"] == "addressee"
    assert response_data["brief_content"] == "brief content"
    assert response_data["case_prod_number"] == "case prod number"
    assert response_data["main_text"] == "main text"

    search_data = response_data["search_data"]
    assert search_data["cypher"] == "cypher"
    assert search_data["fund"] == "fund"
    assert search_data["inventory"] == "inventory"
    assert search_data["case"] == "case"
    assert search_data["leaf"] == "leaf"
    assert search_data["authenticity"] == "authenticity"
    assert search_data["lang"] == "lang"
    assert search_data["playback_method"] == "playback method"

    with open(f"files/{response_data['file_urls'][0]}", "rb") as f:
        file_content = f.read()
        assert file_content == b"file data"

    with open(f"files/{response_data['file_urls'][1]}", "rb") as f_2:
        file_content_2 = f_2.read()
        assert file_content_2 == b"file data"

    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
    
    await engine.dispose()
    os.remove(f"files/{response_data['file_urls'][0]}")
    os.remove(f"files/{response_data['file_urls'][1]}")


# @pytest.mark.asyncio
# async def test_create_with_unsupported_files_document_handler(
#     init_engine,
#     get_user_client, 
#     get_document_client,
#     get_user, 
#     upload_admin_user_to_db,
#     get_document_dict
# ):
#     engine = init_engine
#     async with engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
#         await conn.run_sync(mapper_registry.metadata.create_all)

#     user = get_user
#     await upload_admin_user_to_db(user)

#     client = get_user_client
#     document_client = get_document_client
#     response = await client.login(email="test@email.com", password="password")
#     access_token = response.json()["access_token"]

#     file_url = 'file_1.pdf'
#     file_url_2 = 'file_2.mp4'
#     unsupported_format = 'video/mp4'

#     files = [
#         ("files", (file_url, b"file data", 'application/pdf')),
#         ("files", (file_url_2, b"file data", unsupported_format))
#     ]

#     response = await document_client.create_document_handler(
#         token=access_token,
#         files=files,
#         data=get_document_dict
#     )

#     response_data = response.json()

#     assert response_data['detail'] == f"Unsupported format {unsupported_format}. Allowed formats: png, jpg, jpeg, doc, docs, pdf"

#     async with engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
    
#     await engine.dispose()