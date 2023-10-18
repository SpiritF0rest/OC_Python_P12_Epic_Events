import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Role, User
from epic_events.views.generic_view import display_missing_data, display_exception
from epic_events.views.user_view import display_user_already_exists, display_incorrect_role, display_user_created


@click.group()
@click.pass_context
@check_auth
def user(ctx):
    ctx.ensure_object(dict)


@user.command()
@click.option("-n", "--name", required=True, type=str)
@click.option("-e", "--email", required=True, type=str)
@click.option("-r", "--role", required=True, type=str)
@click.password_option()
@click.pass_context
@has_permission(roles=["management"])
def create_user(session, name, email, password, role):
    if not name and email and password and role:
        return display_missing_data()
    if session.scalar(select(User).where(User.email == email)):
        return display_user_already_exists(email)
    new_user_role = session.scalar(select(Role).where(Role.name == role))
    if not new_user_role:
        return display_incorrect_role(role)
    try:
        new_user = User(name=name,
                        email=email,
                        role=new_user_role.id)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        return display_user_created(email)
    except Exception as e:
        return display_exception(e)


@user.command()
def update_user():
    pass


@user.command()
def get_user():
    pass


@user.command()
def delete_user():
    pass
