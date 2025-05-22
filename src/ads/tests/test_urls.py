import pytest
from django.urls import reverse
from ads.models import Ad, Category, ExchangeProposal
from users.models import User


@pytest.fixture
def user1():
    return User.objects.create_user(email="user1@example.com", password="pass", first_name="User", last_name="One")


@pytest.fixture
def user2():
    return User.objects.create_user(email="user2@example.com", password="pass", first_name="User", last_name="Two")


@pytest.fixture
def category():
    return Category.objects.create(title="Категория1")


@pytest.fixture
def ad1(user1, category):
    return Ad.objects.create(
        user=user1,
        title="Тестовое объявление 1",
        description="Описание 1",
        category=category,
        condition="new",
    )


@pytest.fixture
def ad2(user2, category):
    return Ad.objects.create(
        user=user2,
        title="Тестовое объявление 2",
        description="Описание 2",
        category=category,
        condition="used",
    )


@pytest.mark.django_db
# @pytest.mark.skip
def test_create_ad(client, user1, category):
    # Авторизация пользователя
    client.force_login(user1)

    url = reverse("ads:ad-create")  # Укажи правильный namespace и name
    data = {
        "title": "Новое объявление",
        "description": "Описание товара",
        "image_url": "",  # если поле image_url опционально и принимает пустую строку
        "category": category.id,
        "condition": "new",
    }
    response = client.post(url, data)

    # Проверяем редирект (обычно после успешного создания)
    assert response.status_code in (302, 201)

    # Проверяем, что объявление создалось
    ad = Ad.objects.filter(title="Новое объявление").first()
    assert ad is not None
    assert ad.user == user1
    assert ad.category == category


@pytest.mark.django_db
# @pytest.mark.skip
def test_edit_ad(client, user1, user2, ad1):
    url = reverse("ads:ad-edit", args=[ad1.id])

    # Попытка редактировать без авторизации
    response = client.post(url, {"title": "Измененный заголовок"})
    assert response.status_code in (302, 403, 401)  # может быть редирект на логин или запрет

    # Логиним пользователя, который не владелец — не должен иметь доступа
    client.force_login(user2)
    response = client.post(url, {"title": "Измененный заголовок"})
    assert response.status_code in (403, 404)  # доступ запрещен или объект не найден

    # Логиним владельца и меняем объявление
    client.logout()
    client.force_login(user1)
    response = client.post(url, {
        "title": "Измененный заголовок",
        "description": ad1.description,
        "category": ad1.category.id,
        "condition": ad1.condition,
    })
    assert response.status_code in (302, 200)

    ad1.refresh_from_db()
    assert ad1.title == "Измененный заголовок"


@pytest.mark.django_db
# @pytest.mark.skip
def test_delete_ad(client, user1, user2, ad1):
    url = reverse("ads:ad-delete", args=[ad1.id])

    # Неавторизованный пользователь — редирект или отказ
    response = client.post(url)
    assert response.status_code in (302, 401, 403)

    # Не владелец
    client.force_login(user2)
    response = client.post(url)
    assert response.status_code in (403, 404)

    # Владелец удаляет
    client.logout()
    client.force_login(user1)
    response = client.post(url)
    assert response.status_code in (302, 200)

    # Проверяем удаление
    with pytest.raises(Ad.DoesNotExist):
        Ad.objects.get(id=ad1.id)


@pytest.mark.django_db
# @pytest.mark.skip
def test_search_filter_pagination(client, user1, category):
    client.force_login(user1)

    # Создаем несколько объявлений
    for i in range(15):
        Ad.objects.create(
            user=user1,
            title=f"Товар {i}",
            description="Тестовое описание",
            category=category,
            condition="new" if i % 2 == 0 else "used",
        )

    url = reverse("ads:ad-list")  # Или как у тебя называется URL списка объявлений

    # Тест поиска по ключевым словам
    response = client.get(url, {"q": "Товар 1"})
    assert response.status_code == 200
    assert "Товар 1" in response.content.decode()

    # Тест фильтрации по категории
    response = client.get(url, {"category": category.id})
    assert response.status_code == 200

    # Тест фильтрации по состоянию
    response = client.get(url, {"condition": "new"})
    assert response.status_code == 200

    # Тест пагинации: по умолчанию 10 на странице
    response = client.get(url, {"page": 2})
    assert response.status_code == 200


@pytest.mark.django_db
# @pytest.mark.skip
def test_create_exchange_proposal(client, user1, user2, ad1, ad2):
    client.force_login(user1)

    url = reverse("ads:exchange-create")  # Укажи правильный URL name
    data = {
        "ad_sender": ad1.id,
        "ad_receiver": ad2.id,
        "comment": "Предлагаю обменяться",
    }

    response = client.post(url, data)
    assert response.status_code in (302, 201)

    proposal = ExchangeProposal.objects.filter(ad_sender=ad1, ad_receiver=ad2).first()
    assert proposal is not None
    assert proposal.comment == "Предлагаю обменяться"
    assert proposal.status == "ожидает"


@pytest.mark.django_db
@pytest.mark.skip
def test_update_exchange_proposal_status(client, user1, user2, ad1, ad2):
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad1,
        ad_receiver=ad2,
        comment="Обменяемся?",
    )

    client.force_login(user1)
    url = reverse("ads:exchange-update", args=[proposal.id])
    data = {"status": "принята"}

    response = client.post(url, data)
    assert response.status_code in (302, 200)

    proposal.refresh_from_db()
    assert proposal.status == "принята"


@pytest.mark.django_db
# @pytest.mark.skip
def test_filter_exchange_proposals(client, user1, user2, ad1, ad2):
    ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2, status="ожидает")
    ExchangeProposal.objects.create(ad_sender=ad2, ad_receiver=ad1, status="принята")

    client.force_login(user1)
    url = reverse("ads:exchange-list")  # Укажи правильный URL

    response = client.get(url, {"status": "ожидает"})
    assert response.status_code == 200
    assert "ожидает" in response.content.decode()

    response = client.get(url, {"ad_sender": ad1.id})
    assert response.status_code == 200

    response = client.get(url, {"ad_receiver": ad2.id})
    assert response.status_code == 200


@pytest.mark.django_db
# @pytest.mark.skip
def test_view_ads_list(client, user1, category):
    client.force_login(user1)
    url = reverse("ads:ad-list")  # Или нужный URL

    response = client.get(url)
    assert response.status_code == 200
    # Можно проверить, что в ответе есть поле title (примитивно)
    assert "Объявления" in response.content.decode()
