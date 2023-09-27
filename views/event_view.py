import click


@click.group()
def cli_event():
    pass


@cli_event.command()
def create_event():
    pass


@cli_event.command()
def update_event():
    pass


@cli_event.command()
def list_events():
    pass


@cli_event.command()
def get_event():
    pass


@cli_event.command()
def delete_event():
    pass
