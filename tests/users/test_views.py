from faker import Faker

from tests.fixtures import users  # noqa F401

fake = Faker()


def test_users_list(client, users):  # noqa F811
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.template.name == "users/list.html"
    assert "request" in response.context
    assert "users" in response.context


def test_user_create_init(client):
    response = client.get("/users/create/")
    assert response.status_code == 200
    assert response.template.name == "users/form.html"
    assert "request" in response.context
    assert "form_data" in response.context
    assert 'id="email"' in response.content.decode("utf-8")
    assert 'id="full_name"' in response.content.decode("utf-8")


def test_user_create_valid_submit(client):
    data = {"full_name": fake.name(), "email": fake.email()}
    response = client.post("/users/create/", data=data)
    assert response.status_code == 200
    assert response.url == "http://testserver/users/"

    response = client.get("/users/")
    assert response.status_code == 200
    assert "users" in response.context
    assert len(response.context["users"]) == 1
    assert response.context["users"][0].email == data["email"]
    assert response.context["users"][0].full_name == data["full_name"]


def test_user_create_invalid_submit(client):
    data = {"full_name": fake.name(), "email": "invalid_email"}
    response = client.post("/users/create/", data=data)
    assert response.status_code == 200
    assert response.url == "http://testserver/users/create/"
    assert {"email": "value is not a valid email address"} == response.context["errors"]
    assert data == dict(response.context["form_data"])
