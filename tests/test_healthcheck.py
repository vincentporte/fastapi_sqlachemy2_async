def test_healthcheck(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}
