import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_analysis(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/v1/analysis/",
        json={
            "code_content": "def hello():\n    print('Hello, World!')",
            "language": "python",
            "file_name": "hello.py",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["language"] == "python"
    assert data["status"] == "completed"
    assert "overall_score" in data
    assert "grade" in data


@pytest.mark.asyncio
async def test_create_analysis_security_issues(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/v1/analysis/",
        json={
            "code_content": "password = 'admin123'\nresult = eval(user_input)",
            "language": "python",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data.get("scores", {})) > 0


@pytest.mark.asyncio
async def test_list_analyses(client: AsyncClient, auth_headers: dict):
    await client.post(
        "/api/v1/analysis/",
        json={"code_content": "x = 1", "language": "python"},
        headers=auth_headers,
    )

    response = await client.get("/api/v1/analysis/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_analysis(client: AsyncClient, auth_headers: dict):
    create_response = await client.post(
        "/api/v1/analysis/",
        json={"code_content": "x = 1", "language": "python"},
        headers=auth_headers,
    )
    analysis_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/analysis/{analysis_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == analysis_id


@pytest.mark.asyncio
async def test_get_analysis_not_found(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/api/v1/analysis/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_analysis_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/analysis/",
        json={"code_content": "x = 1", "language": "python"},
    )
    assert response.status_code == 403
