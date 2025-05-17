import httpx
from core.config import (
    BASEROW_URL,
    BASEROW_TOKEN,
    BASEROW_EMAIL,
    BASEROW_PASSWORD,
)


# login to the user baserow account
async def auth_user() -> str:
    payload = {"email": BASEROW_EMAIL, "password": BASEROW_PASSWORD}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASEROW_URL}/api/user/token-auth/", data=payload
        )
        response.raise_for_status()
        json_data = response.json()
        return json_data["token"]


async def create_table(table_name: str) -> str:
    # Prepare the request payload
    HEADERS = {
        "Authorization": f"JWT {await auth_user()}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": table_name,
    }

    # create the table if it does not exist
    endpoint = f"{BASEROW_URL}/api/database/tables/database/197/"
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=HEADERS)
        for x in response.json():
            if x["name"] == payload["name"]:
                return x["id"]

    # remove the first two rows of the table
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, headers=HEADERS, json=payload)
        json_data = response.json()
        table_id = json_data["id"]
        for row_id in [1, 2]:
            await client.delete(
                f"{BASEROW_URL}/api/database/rows/table/{table_id}/{row_id}/",
                headers={"Authorization": f"Token {BASEROW_TOKEN}"},
            )

        return table_id


async def update_fields(table_id: int):
    print(f"Table id - {table_id}")
    HEADERS = {
        "Authorization": f"JWT {await auth_user()}",
        "Content-Type": "application/json",
    }
    # Prepare the request payload
    fields = [
        {"name": "Date Scraped", "type": "text"},
        {"name": "Date Of Article", "type": "text"},
        {"name": "News Article", "type": "text"},
        {"name": "Link", "type": "url"},
        {"name": "Suspect Name", "type": "text"},
        {"name": "Charges", "type": "text"},
        {"name": "Primary Keywords", "type": "text"},
        {"name": "Secondary Keywords", "type": "text"},
    ]

    # go through eash field and verify their existence in the database
    async with httpx.AsyncClient() as client:
        for field in fields:
            endpoint = f"{BASEROW_URL}/api/database/fields/table/{table_id}/"
            response = await client.post(endpoint, headers=HEADERS, json=field)
            json_data = response.json()
            if json_data.get("error") == "ERROR_FIELD_WITH_SAME_NAME_ALREADY_EXISTS":
                continue

        # change the primary key of the table
        response = await client.get(
            f"{BASEROW_URL}/api/database/fields/table/{table_id}/", headers=HEADERS
        )
        for field in response.json():
            if field["name"] == "Date Scraped":
                await client.post(
                    f"{BASEROW_URL}/api/database/fields/table/{table_id}/change-primary-field/",
                    json={"new_primary_field_id": field["id"]},
                    headers=HEADERS,
                )

        # delete unwanted columns
        for field in response.json():
            if field["name"] in ["Name", "Notes", "Active"]:
                await client.delete(
                    f"{BASEROW_URL}/api/database/fields/{field['id']}/", headers=HEADERS
                )
        return table_id


# Headers for authentication and content type
async def add_data(table_name: str, data: dict):
    table_id = await create_table(table_name)
    print(f"Table_ID: {table_id}")
    table_id = await update_fields(table_id)
    # baserow = BaserowApi(database_url=BASEROW_URL, token=BASEROW_TOKEN)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASEROW_URL}/api/database/rows/table/{table_id}/?user_field_names=true",
            headers={
                "Authorization": f"Token {BASEROW_TOKEN}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        print(response.text)
