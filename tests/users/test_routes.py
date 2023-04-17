from faker import Faker

from tests.fixtures import user, users  # noqa F401

faker = Faker()


def test_create_user(client):
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/users/create/",
        json={"email": "test@example.com", "full_name": "Full Name Test"},
    )
    assert response.status_code == 200
    assert response.json().get("email") == "test@example.com"
    assert response.json().get("full_name") == "Full Name Test"

    # verify that the user is added to the database
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_user_with_duplicated_email(client, user):  # noqa F811
    response = client.post(
        "/api/users/create/",
        json={"email": user.email, "full_name": "Full Name Test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_get_user(client, user):  # noqa F811
    response = client.get(f"/api/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
    }


def test_get_user_with_notuuid(client):
    response = client.get("/api/users/notuuid")
    assert response.status_code == 400


def test_get_user_with_unexistant_id(client):
    uuid = faker.uuid4()
    response = client.get(f"/api/users/{uuid}")
    assert response.status_code == 404


def test_update_user(client, user):  # noqa F811
    email = faker.email()
    full_name = faker.name()
    response = client.patch(f"/api/users/{user.id}", json={"email": email, "full_name": full_name})
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "full_name": full_name,
        "id": user.id,
    }


def test_update_user_with_duplicated_email(client, users):  # noqa F811
    response = client.patch(f"/api/users/{users[0].id}", json={"email": users[1].email})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}


def test_delete_user(client, user):  # noqa F811
    response = client.delete(f"/api/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"User {user.email} deleted successfully"}

    response = client.delete(f"/api/users/{user.id}")
    assert response.status_code == 404
