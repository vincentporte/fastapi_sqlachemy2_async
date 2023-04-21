from faker import Faker

from tests.fixtures import organizations  # noqa F401

fake = Faker()


def test_organizations_list(client, organizations):  # noqa F811
    response = client.get("/organizations/")
    assert response.status_code == 200
    assert response.template.name == "organizations/list.html"
    assert "request" in response.context
    assert "organizations" in response.context


def test_organization_create_init(client):
    response = client.get("/organizations/create/")
    assert response.status_code == 200
    assert response.template.name == "organizations/form.html"
    assert "request" in response.context
    assert "form_data" in response.context
    assert 'id="email"' in response.content.decode("utf-8")
    assert 'id="full_name"' in response.content.decode("utf-8")


def test_organization_create_valid_submit(client):
    data = {"full_name": fake.name(), "email": fake.email()}
    response = client.post("/organizations/create/", data=data)
    assert response.status_code == 200
    assert response.url == "http://testserver/organizations/"

    response = client.get("/organizations/")
    assert response.status_code == 200
    assert "organizations" in response.context
    assert len(response.context["organizations"]) == 1
    assert response.context["organizations"][0].email == data["email"]
    assert response.context["organizations"][0].full_name == data["full_name"]


def test_organization_create_invalid_submit(client):
    data = {"full_name": fake.name(), "email": "invalid_email"}
    response = client.post("/organizations/create/", data=data)
    assert response.status_code == 200
    assert response.url == "http://testserver/organizations/create/"
    assert {"email": "value is not a valid email address"} == response.context["errors"]
    assert data == dict(response.context["form_data"])
