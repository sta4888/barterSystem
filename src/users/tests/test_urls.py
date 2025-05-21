import pytest
from django.urls import reverse, resolve
from users.views import RegisterView, LoginView, LogoutView
from django.test import Client


@pytest.mark.django_db
def test_register_url():
    url = reverse("users:register")
    view = resolve(url)
    assert view.func.view_class == RegisterView

    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert "users/register.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_login_url():
    url = reverse("users:login")
    view = resolve(url)
    assert view.func.view_class == LoginView

    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert "users/login.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_logout_url_redirects():
    url = reverse("users:logout")
    view = resolve(url)
    assert view.func.view_class == LogoutView

    client = Client()
    response = client.get(url)
    # LogoutView делает redirect на login, статус 302
    assert response.status_code == 302
    assert response.url == reverse("users:login")
