from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions

from ads.models import Category, Ad, ExchangeProposal
from .serializers import CategorySerializer, AdSerializer, ExchangeProposalSerializer


@extend_schema(summary="Список категорий", description="Возвращает все категории объявлений.")
class CategoryListAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(
    list=extend_schema(summary="Список объявлений", description="Возвращает список всех объявлений."),
    create=extend_schema(summary="Создание объявления"),
)
class AdListAPI(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(summary="Детали/обновление/удаление объявления")
class AdDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema_view(
    list=extend_schema(summary="Список предложений обмена"),
    create=extend_schema(summary="Создание предложения обмена"),
)
class ExchangeProposalListAPI(generics.ListCreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@extend_schema(summary="Детали/обновление/удаление предложения обмена")
class ExchangeProposalDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
