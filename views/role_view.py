import click


@click.group()
def cli_role():
    pass


@cli_role.command()
def create_role():
    pass


@cli_role.command()
def list_role():
    pass
