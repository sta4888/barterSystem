import pytest
from django.urls import reverse
from users.models import User


@pytest.mark.django_db
# @pytest.mark.skip
def test_register_view(client):
    response = client.post(reverse("users:register"), {
        "first_name": "John",
        "last_name": "Doe",
        "middle_name": "Smith",
        "email": "john@example.com",
        "phone": "1234567890",
        "password1": "strongpassword123",
        "password2": "strongpassword123",
    })
    user = User.objects.get(email="john@example.com")
    assert user
    assert response.status_code == 302  # redirect after success
    assert user.check_password("strongpassword123")


@pytest.mark.django_db
def test_login_view(client):
    user = User.objects.create_user(
        email="jane@example.com", password="secure123",
        first_name="Jane", last_name="Doe"
    )
    response = client.post(reverse("users:login"), {
        "username": "jane@example.com",
        "password": "secure123",
    })
    assert response.status_code == 302  # redirect on success
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_logout_view(client):
    user = User.objects.create_user(
        email="jane@example.com", password="secure123",
        first_name="Jane", last_name="Doe"
    )
    client.login(email="jane@example.com", password="secure123")
    response = client.get(reverse("users:logout"))
    assert response.status_code == 302
    assert "_auth_user_id" not in client.session
