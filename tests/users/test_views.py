def test_create_user(client):
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/users/create/",
        json={"email": "test@example.com", "full_name": "Full Name Test"},
    )
    assert response.status_code == 200

    response = client.get(f"/api/users/{response.json().get('id')}")
    assert response.status_code == 200
    assert response.json() == {
        "id": response.json().get("id"),
        "email": "test@example.com",
        "full_name": "Full Name Test",
    }

    response = client.get("/api/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
