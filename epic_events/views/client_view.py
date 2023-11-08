from click import ClickException


def display_unknown_client():
    raise ClickException("Sorry, this client does not exist.")


def display_client_data(data):
    print(data)


def display_clients_list(clients):
    for client in clients:
        print(f"Id: {client.id}, name: {client.name}, email: {client.email}, phone: {client.phone}, "
              f"company: {client.company}, contact_id: {client.commercial_contact_id}")


def display_client_already_exists(email):
    raise ClickException(f"Client ({email}) already exists.")


def display_client_created(email):
    print(f"Client {email} is successfully created.")


def display_client_updated(email):
    print(f"Client {email} is successfully updated.")


def display_client_deleted():
    print(f"This client is successfully deleted.")
