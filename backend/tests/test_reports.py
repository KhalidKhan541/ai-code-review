import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_report(client: AsyncClient, auth_headers: dict):
    create_response = await client.post(
        "/api/v1/analysis/",
        json={"code_content": "x = 1", "language": "python"},
        headers=auth_headers,
    )
    analysis_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/reports/{analysis_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data


@pytest.mark.asyncio
async def test_get_report_not_found(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/api/v1/reports/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_issues(client: AsyncClient, auth_headers: dict):
    create_response = await client.post(
        "/api/v1/analysis/",
        json={"code_content": "eval('malicious')", "language": "python"},
        headers=auth_headers,
    )
    analysis_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/reports/{analysis_id}/issues", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
