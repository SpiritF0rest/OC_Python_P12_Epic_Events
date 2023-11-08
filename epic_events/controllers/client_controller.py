from datetime import datetime

import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Client
from epic_events.views.client_view import display_unknown_client, display_client_data, \
    display_clients_list, display_client_already_exists, display_client_created, display_client_updated, \
    display_client_deleted
from epic_events.views.generic_view import display_exception, display_missing_data, display_no_data_to_update
from epic_events.views.permissions_view import display_not_authorized


@click.group()
@click.pass_context
@check_auth
def client(ctx):
    ctx.ensure_object(dict)


@client.command(name="list")
@click.option("-c", "--contact_id", required=False, type=int)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def list_clients(session, ctx, contact_id):
    try:
        query = select(Client)
        if contact_id:
            query = query.where(Client.commercial_contact_id == contact_id)
        clients = session.scalars(query.order_by(Client.name))
        return display_clients_list(clients)
    except Exception as e:
        return display_exception(e)


@client.command(name="get")
@click.option("-id", "--client_id", required=True, type=int)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def get_client(session, ctx,  client_id):
    if not client_id:
        return display_missing_data()
    selected_client = session.scalar(select(Client).where(Client.id == client_id))
    if not selected_client:
        return display_unknown_client()
    return display_client_data(selected_client)


@client.command(name="create")
@click.option("-e", "--email", required=True, type=str)
@click.option("-n", "--name", required=False, type=str)
@click.option("-ph", "--phone", required=False, type=int)
@click.option("-c", "--company", required=False, type=int)
@click.pass_context
@has_permission(["commercial"])
def create_client(session, ctx, email, name, phone, company):
    if not email:
        return display_missing_data()
    if session.scalar(select(Client).where(Client.email == email)):
        return display_client_already_exists(email)
    try:
        date_now = datetime.now()
        new_client = Client(email=email,
                            creation_date=date_now,
                            update_date=date_now,
                            commercial_contact_id=ctx.obj["current_user"].id)
        new_client.name = name if name else None
        new_client.phone = phone if phone else None
        new_client.company = company if company else None
        session.add(new_client)
        session.commit()
        return display_client_created(email)
    except Exception as e:
        return display_exception(e)


@client.command(name="update")
@click.option("-id", "--client_id", required=True, type=int)
@click.option("-e", "--email", required=False, type=str)
@click.option("-n", "--name", required=False, type=str)
@click.option("-ph", "--phone", required=False, type=int)
@click.option("-c", "--company", required=False, type=int)
@click.pass_context
@has_permission(["commercial"])
def update_client(session, ctx, client_id, email, name, phone, company):
    if not client_id:
        return display_missing_data()
    if not (email or name or phone or company):
        return display_no_data_to_update()
    requester = ctx.obj["current_user"].id
    selected_client = session.scalar(select(Client).where(Client.id == client_id))
    if not selected_client:
        return display_unknown_client()
    if selected_client.commercial_contact_id != requester:
        return display_not_authorized()
    if email and session.scalar(select(Client).where(Client.email == email)):
        return display_client_already_exists(email)
    try:
        date_now = datetime.now()
        selected_client.email = email if email else selected_client.email
        selected_client.name = name if name else selected_client.name
        selected_client.phone = phone if phone else selected_client.phone
        selected_client.company = company if company else selected_client.company
        selected_client.update_date = date_now
        session.commit()
        return display_client_updated(selected_client.email)
    except Exception as e:
        print(type(e))
        return display_exception(e)


@client.command(name="delete")
@click.option("-id", "--client_id", required=True, type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this client?")
@click.pass_context
@has_permission(roles=["commercial"])
def delete_client(session, ctx, client_id):
    requester = ctx.obj["current_user"].id
    selected_client = session.scalar(select(Client).where(Client.id == client_id))
    if not selected_client:
        return display_unknown_client()
    if selected_client.commercial_contact_id != requester:
        return display_not_authorized()
    try:
        session.delete(selected_client)
        session.commit()
        return display_client_deleted()
    except Exception as e:
        return display_exception(e)
