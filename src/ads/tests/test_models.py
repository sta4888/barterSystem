import pytest

from ads.models import Category, Ad, ExchangeProposal
from users.models import User


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="test@example.com", password="pass", first_name="Test", last_name="User"
    )


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(title="Электроника")
    assert str(category) == "Электроника"
    assert category.title == "Электроника"


@pytest.mark.django_db
def test_ad_creation(test_user):
    user = test_user
    category = Category.objects.create(title="Одежда")

    ad = Ad.objects.create(
        user=user,
        title="Куртка",
        description="Теплая зимняя куртка",
        image_url=None,
        category=category,
        condition="used",
    )

    assert ad.user == user
    assert ad.title == "Куртка"
    assert ad.condition == "used"
    assert ad.category == category
    assert ad.created_at is not None
    assert str(ad) == "Куртка"


@pytest.mark.django_db
def test_exchange_proposal_creation_with_default_status():
    user1 = User.objects.create_user(email="user1@example.com", password="pass", first_name="User", last_name="One")
    user2 = User.objects.create_user(email="user2@example.com", password="pass", first_name="User", last_name="Two")
    category = Category.objects.create(title="Игрушки")

    ad1 = Ad.objects.create(
        user=user1,
        title="Плюшевый мишка",
        description="Большой мягкий мишка",
        category=category,
        condition="new",
    )
    ad2 = Ad.objects.create(
        user=user2,
        title="Конструктор LEGO",
        description="Оригинальный набор",
        category=category,
        condition="used",
    )

    proposal = ExchangeProposal.objects.create(
        ad_sender=ad1,
        ad_receiver=ad2,
        comment="Обменяемся?",
    )

    assert proposal.ad_sender == ad1
    assert proposal.ad_receiver == ad2
    assert proposal.status == "ожидает"
    assert proposal.comment == "Обменяемся?"
    assert proposal.created_at is not None
    assert str(proposal) == f"{ad1} → {ad2} [ожидает]"
