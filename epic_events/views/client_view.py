from click import ClickException


def display_unknown_client():
    raise ClickException("Sorry, this client does not exist.")


def display_client_data(data):
    print(data)


def display_clients_list(clients):
    print(clients)
