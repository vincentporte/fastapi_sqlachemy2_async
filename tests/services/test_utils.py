from app.services.utils import get_errors_dict


def test_get_errors_dict():
    errors = [{"loc": ("email",), "msg": "value is not a valid email address", "type": "value_error.email"}]
    errors_dict = get_errors_dict(errors)
    assert errors_dict == {"email": "value is not a valid email address"}
