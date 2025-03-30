import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_audio(client: AsyncClient, user_headers):
    _, headers = user_headers
    file_data = {
        "file": ("test_audio.mp3", b"dummy_audio_data", "audio/mpeg")
    }

    response = await client.post(
        "/files/upload/",
        files=file_data,
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json() == "The file was saved successfully"


@pytest.mark.asyncio
async def test_get_list_files(client: AsyncClient, audio_file, user_headers):
    _, headers = user_headers
    response = await client.get("/files/", headers=headers)

    assert response.status_code == 200
    files = response.json()
    assert len(files) == 3
    for file, expected_file in zip(files, audio_file):
        assert file["filename"] == expected_file.filename
        assert file["filepath"] == expected_file.filepath


@pytest.mark.asyncio
async def test_get_no_files(client: AsyncClient, user_headers):
    _, headers = user_headers
    response = await client.get("/files/", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "No files found for this user"}
