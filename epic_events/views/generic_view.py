from click import ClickException


def display_missing_data():
    raise ClickException("Missing data in the command")


def display_exception(e):
    raise ClickException(f"Error: {e}") from e
