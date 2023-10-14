from click import ClickException


def display_missing_data():
    raise ClickException("Missing data in the command.")


def display_unknown_client():
    raise ClickException("Sorry, this client does not exist.")


def display_client_data(data):
    print(data)


def display_clients_list(clients):
    print(clients)
