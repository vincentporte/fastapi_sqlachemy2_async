from tests.fixtures import users  # noqa F401


def test_users_list(client, users):  # noqa F811
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.template.name == "users/list.html"
    assert "request" in response.context
    assert "users" in response.context
