import click


@click.group()
def cli_contract():
    pass


@cli_contract.command()
def create_contract():
    pass


@cli_contract.command()
def update_contract():
    pass


@cli_contract.command()
def list_contracts():
    pass


@cli_contract.command()
def get_contract():
    pass


@cli_contract.command()
def delete_contract():
    pass
