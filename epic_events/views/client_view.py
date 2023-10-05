import click


@click.group()
def cli_client():
    pass


@cli_client.command()
def create_client():
    pass


@cli_client.command()
def update_client():
    pass


@cli_client.command()
def list_clients():
    pass


@cli_client.command()
def get_client():
    pass


@cli_client.command()
def delete_client():
    pass
