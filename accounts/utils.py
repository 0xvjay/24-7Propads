import re


def is_valid_phone(phone: str):
    """
    Checks if the given phone number is a valid Indian phone number.

    Args:
        phone: The phone number to validate.

    Returns:
        True if the phone number is valid, False otherwise.
    """
    regex = r"^\+91-^[6-9]\d{9}$"
    match = re.match(regex, phone)
    return bool(match)
