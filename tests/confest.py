import pytest

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass

@pytest.fixture()
def get_test_user():
    return {
        "user":
            {
                "username": "test_user",
                "email": "test_email@sobaka.ru",
                "telephone": "telephone",
                "age": 11,
                "balance": "0",
                "role": "Customer",
                "password": "test_password",
            }
    }
