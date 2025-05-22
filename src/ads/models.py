from django.db import models
from django.urls import reverse

from users.models import User
from .mixins import TimestampMixin


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название категории")

    def __str__(self):
        return self.title


class Ad(TimestampMixin):
    CONDITION_CHOICES = [
        ("new", "Новый"),
        ("used", "Б/у"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image_url = models.ImageField(
        upload_to="ads/image/",
        verbose_name="Фото",
        null=True,
        blank=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        verbose_name="Состояние товара"
    )

    def get_absolute_url(self):
        return reverse('ads:ad-detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class ExchangeProposal(TimestampMixin):
    STATUS_CHOICES = (
        ("ожидает", "Ожидает"),
        ("принята", "Принята"),
        ("отклонена", "Отклонена"),
    )

    ad_sender = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="sent_proposals", verbose_name="Отправитель"
    )
    ad_receiver = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="received_proposals", verbose_name="Получатель"
    )
    comment = models.TextField(verbose_name="Комментарий")
    status = models.CharField(choices=STATUS_CHOICES, default="ожидает", max_length=150, verbose_name="Статус")

    def __str__(self):
        return f"{self.ad_sender} → {self.ad_receiver} [{self.status}]"
