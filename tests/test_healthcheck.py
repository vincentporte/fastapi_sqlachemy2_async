def test_healthcheck(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}
