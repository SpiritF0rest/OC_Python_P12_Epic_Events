import pytest

from epic_events.models.base import Base

from datetime import datetime


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
                "name": "alex",
                "email": "manager_alex@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
                "role": 1
            },
            {
                "id": 2,
                "name": "antony",
                "email": "support_antony@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
                "role": 2
            },
            {
                "id": 3,
                "name": "angie",
                "email": "commercial_angie@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr+xJC+T5vqPY",
                "role": 3
            }
        ]),
        ("clients", [
            {
                "id": 1,
                "name": "client",
                "email": "client@test.com",
                "phone": "0123456789",
                "company": "shop",
                "creation_date": datetime(2023, 9, 24, 14, 30, 0),
                "update_date": datetime(2023, 9, 24, 14, 30, 0),
                "commercial_contact_id": 3
            }
        ]),
        ("contracts", [
            {
                "id": 1,
                "client_id": 1,
                "total_amount": 100,
                "left_to_pay": 20,
                "status": "SIGNED",
                "creation_date": datetime(2023, 9, 24, 14, 30, 0),
                "update_date": datetime(2023, 9, 24, 14, 30, 0),
                "commercial_contact_id": 3
            },
            {
                "id": 2,
                "client_id": 1,
                "total_amount": 100,
                "left_to_pay": 0,
                "status": "UNSIGNED",
                "creation_date": datetime(2023, 9, 24, 14, 30, 0),
                "update_date": datetime(2023, 9, 24, 14, 30, 0),
                "commercial_contact_id": 3
            },
        ]),
        ("events", [
            {
                "id": 1,
                "contract_id": 1,
                "client_id": 1,
                "start_date": datetime(2023, 10, 24, 14, 30, 0),
                "end_date": datetime(2023, 10, 25, 14, 30, 0),
                "support_contact_id": 3,
                "location": "Paris",
                "attendees": 20,
                "notes": "Lorem ipsum",
                "creation_date": datetime(2023, 9, 24, 14, 30, 0),
                "update_date": datetime(2023, 9, 24, 14, 30, 0),

            },
        ])
    ]
