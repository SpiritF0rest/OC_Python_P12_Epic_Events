from click import ClickException


def display_successful_connection():
    print("Connection successful.")


def display_auth_data_entry_error():
    raise ClickException("Please, be sure to use the correct email and password.")


def display_auth_already_connected():
    raise ClickException("You are already connected.")


def display_invalid_token():
    raise ClickException("Invalid token")


def display_not_connected_error():
    raise ClickException("Please log in first.")
