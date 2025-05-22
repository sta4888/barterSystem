import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from ads.models import Ad, Category, ExchangeProposal
from users.models import User

@pytest.mark.django_db
class TestAdsAPI:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="testuser@example.com",
            password="strongpassword",
            first_name="Test",
            last_name="User"
        )

    @pytest.fixture
    def category(self):
        return Category.objects.create(title="Электроника")

    @pytest.fixture
    def ad(self, user, category):
        return Ad.objects.create(
            user=user,
            title="Телефон iPhone",
            description="Очень хороший телефон",
            category=category,
            condition="used"
        )

    def test_get_ads_list(self, api_client, ad):
        url = reverse("api:api-ads")
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["title"] == ad.title

    def test_create_ad_requires_auth(self, api_client, category):
        url = reverse("api:api-ads")
        data = {
            "title": "Новый ноутбук",
            "description": "Очень мощный ноутбук",
            "category": category.id,
            "condition": "new"
        }
        response = api_client.post(url, data, format='json')
        # неавторизованный должен получить 403 или 401
        assert response.status_code in (401, 403)

    def test_create_ad_authenticated(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        url = reverse("api:api-ads")
        data = {
            "title": "Новый ноутбук",
            "description": "Очень мощный ноутбук",
            "category": category.id,
            "condition": "new"
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.json()["title"] == data["title"]

    def test_update_ad(self, api_client, user, ad):
        api_client.force_authenticate(user=user)
        url = reverse("api:api-ad-detail", args=[ad.id])
        new_data = {
            "title": "Обновленное название",
            "description": ad.description,
            "category": ad.category.id,
            "condition": ad.condition
        }
        response = api_client.put(url, new_data, format='json')
        assert response.status_code == 200
        assert response.json()["title"] == "Обновленное название"

@pytest.mark.django_db
class TestExchangeProposalAPI:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user1(self):
        return User.objects.create_user(email="user1@example.com", password="pass123")

    @pytest.fixture
    def user2(self):
        return User.objects.create_user(email="user2@example.com", password="pass123")

    @pytest.fixture
    def category(self):
        return Category.objects.create(title="Игрушки")

    @pytest.fixture
    def ad1(self, user1, category):
        return Ad.objects.create(user=user1, title="Мяч", description="Футбольный мяч", category=category, condition="used")

    @pytest.fixture
    def ad2(self, user2, category):
        return Ad.objects.create(user=user2, title="Кубик Рубика", description="Собираемый кубик", category=category, condition="used")

    @pytest.fixture
    def proposal(self, ad1, ad2):
        return ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2, comment="Обменяемся?")

    def test_list_exchange_proposals(self, api_client, proposal):
        url = reverse("api:api-exchange-list")
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert any(p["id"] == proposal.id for p in data)

    def test_create_exchange_proposal_requires_auth(self, api_client, ad1, ad2):
        url = reverse("api:api-exchange-list")
        data = {
            "ad_sender": ad1.id,
            "ad_receiver": ad2.id,
            "comment": "Обменяемся?",
            "status": "ожидает"
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code in (401, 403)
