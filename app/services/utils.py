from typing import List

ErrorDict = dict


def get_errors_dict(errors: List[ErrorDict]) -> dict:
    """
    Returns a dictionary where the keys are the field names and the values are the error messages.
    """
    errors_dict = {}
    for error in errors:
        field = error["loc"][-1]
        errors_dict[field] = error["msg"]
    return errors_dict
