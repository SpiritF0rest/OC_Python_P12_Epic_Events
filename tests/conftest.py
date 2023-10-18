import pytest

from epic_events.models.base import Base


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    return [
        ("roles", [
            {
                "id": 1,
                "name": "management"
            },
            {
                "id": 2,
                "name": "support"
            },
            {
                "id": 3,
                "name": "commercial"
            }
        ]),
        ("users", [
            {
                "id": 1,
                "name": "toto",
                "email": "manager_toto@test.com",
                "password": "1234",
                "role": 1
            }
        ])]
