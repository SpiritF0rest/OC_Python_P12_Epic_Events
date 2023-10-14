from click import ClickException


def display_user_already_exists(email):
    raise ClickException(f"User ({email}) already exists.")


def display_incorrect_role(role):
    raise ClickException(f"{role} is not a correct role.")


def display_user_created(email):
    print(f"User {email} is successfully created")
