import pytest
from users.models import User

pytestmark = pytest.mark.django_db


def test_create_user():
    user = User.objects.create_user(
        email="testuser@example.com",
        password="strongpassword123",
        first_name="Иван",
        last_name="Иванов",
        middle_name="Иванович",
        phone="1234567890"
    )

    assert user.email == "testuser@example.com"
    assert user.first_name == "Иван"
    assert user.last_name == "Иванов"
    assert user.middle_name == "Иванович"
    assert user.phone == "1234567890"
    assert user.avatar.name is None
    assert user.check_password("strongpassword123")
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_active


def test_create_superuser():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass",
        first_name="Админ",
        last_name="Админов",
    )

    assert admin.is_staff
    assert admin.is_superuser
    assert admin.check_password("adminpass")
