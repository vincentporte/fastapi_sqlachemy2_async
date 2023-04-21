from faker import Faker

from tests.fixtures import organization, organizations  # noqa F401

faker = Faker()


def test_create_organization(client):
    response = client.get("/api/organizations/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/organizations/create/",
        json={"email": "test@example.com", "full_name": "Full Name Test"},
    )
    assert response.status_code == 200
    assert response.json().get("email") == "test@example.com"
    assert response.json().get("full_name") == "Full Name Test"

    # verify that the organization is added to the database
    response = client.get("/api/organizations/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_organization_with_duplicated_email(client, organization):  # noqa F811
    response = client.post(
        "/api/organizations/create/",
        json={"email": organization.email, "full_name": "Full Name Test"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Organization already exists"}


def test_get_organization(client, organization):  # noqa F811
    response = client.get(f"/api/organizations/{organization.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": organization.id,
        "email": organization.email,
        "full_name": organization.full_name,
    }


def test_get_organization_with_notuuid(client):
    response = client.get("/api/organizations/notuuid")
    assert response.status_code == 400


def test_get_organization_with_unexistant_id(client):
    uuid = faker.uuid4()
    response = client.get(f"/api/organizations/{uuid}")
    assert response.status_code == 404


def test_update_organization(client, organization):  # noqa F811
    email = faker.email()
    full_name = faker.name()
    response = client.patch(f"/api/organizations/{organization.id}", json={"email": email, "full_name": full_name})
    assert response.status_code == 200
    assert response.json() == {
        "email": email,
        "full_name": full_name,
        "id": organization.id,
    }


def test_update_organization_with_duplicated_email(client, organizations):  # noqa F811
    response = client.patch(f"/api/organizations/{organizations[0].id}", json={"email": organizations[1].email})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}


def test_delete_organization(client, organization):  # noqa F811
    response = client.delete(f"/api/organizations/{organization.id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Organization {organization.email} deleted successfully"}

    response = client.delete(f"/api/organizations/{organization.id}")
    assert response.status_code == 404
