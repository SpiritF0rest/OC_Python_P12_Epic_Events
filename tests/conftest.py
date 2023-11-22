from datetime import datetime, timedelta

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
                "name": "commercial"
            },
            {
                "id": 2,
                "name": "support"
            },
            {
                "id": 3,
                "name": "management"
            }
        ]),
        ("users", [
            {
                "id": 1,
                "name": "alex",
                "email": "manager_alex@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr"
                            "+xJC+T5vqPY",
                "role": 3
            },
            {
                "id": 2,
                "name": "antony",
                "email": "support_antony@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr"
                            "+xJC+T5vqPY",
                "role": 2
            },
            {
                "id": 3,
                "name": "angie",
                "email": "commercial_angie@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr"
                            "+xJC+T5vqPY",
                "role": 1
            },
            {
                "id": 4,
                "name": "manon",
                "email": "commercial_manon@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr"
                            "+xJC+T5vqPY",
                "role": 1
            },
            {
                "id": 5,
                "name": "jeremy",
                "email": "support_jeremy@test.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$9NJxw0p+9aD3SJIN7cCNfw$u+fLlgVRcqz3h6c9vt1K9rYamP6sSOLr"
                            "+xJC+T5vqPY",
                "role": 2
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
            },
            {
                "id": 2,
                "client_id": 1,
                "total_amount": 100,
                "left_to_pay": 0,
                "status": "UNSIGNED",
                "creation_date": datetime(2023, 9, 24, 14, 30, 0),
                "update_date": datetime(2023, 9, 24, 14, 30, 0),
            },
        ]),
        ("events", [
            {
                "id": 1,
                "contract_id": 1,
                "start_date": (datetime.now() + timedelta(days=1)),
                "end_date": (datetime.now() + timedelta(days=2)),
                "support_contact_id": 2,
                "location": "Paris",
                "attendees": 20,
                "notes": "Lorem ipsum",
                "creation_date": datetime(2023, 9, 24, 14, 30, 0),
                "update_date": datetime(2023, 9, 24, 14, 30, 0),
            },
        ])
    ]
