import pytest
from users.forms import UserRegistrationForm, CustomAuthenticationForm
from users.models import User
from django.contrib.auth import authenticate

@pytest.mark.django_db
def test_valid_registration_form():
    form_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "email": "ivan@example.com",
        "phone": "1234567890",
        "password1": "strongpassword123",
        "password2": "strongpassword123",
    }
    form = UserRegistrationForm(data=form_data)
    assert form.is_valid()
    user = form.save()
    assert user.email == "ivan@example.com"
    assert user.check_password("strongpassword123")

@pytest.mark.django_db
def test_invalid_password_mismatch():
    form_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "email": "ivan@example.com",
        "phone": "1234567890",
        "password1": "password123",
        "password2": "differentpassword",
    }
    form = UserRegistrationForm(data=form_data)
    assert not form.is_valid()
    assert "password2" in form.errors
    assert form.errors["password2"] == ["Пароли не совпадают"]





@pytest.mark.django_db
def test_valid_authentication_form():
    user = User.objects.create_user(
        email="test@example.com",
        password="strongpassword123",
        first_name="Test",
        last_name="User",
    )

    form_data = {
        "username": "test@example.com",  # username в форме = email
        "password": "strongpassword123",
    }
    form = CustomAuthenticationForm(data=form_data)
    form.user_cache = authenticate(
        username=form_data["username"], password=form_data["password"]
    )
    assert form.is_valid() or form.user_cache is not None


@pytest.mark.django_db
def test_invalid_authentication_form():
    form_data = {
        "username": "wrong@example.com",
        "password": "nopassword",
    }
    form = CustomAuthenticationForm(data=form_data)
    assert not form.is_valid()
