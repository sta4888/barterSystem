from django.urls import path
from .views import (
    AdCreateView, AdUpdateView, AdDeleteView, AdListView, AdDetailView,
    ExchangeProposalCreateView, ExchangeProposalListView, ExchangeProposalUpdateView
)

app_name = "ads"

urlpatterns = [
    path('', AdListView.as_view(), name='ad-list'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('ad/create/', AdCreateView.as_view(), name='ad-create'),
    path('ad/<int:pk>/edit/', AdUpdateView.as_view(), name='ad-edit'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),

    path('exchange/create/', ExchangeProposalCreateView.as_view(), name='exchange-create'),
    path('exchange/', ExchangeProposalListView.as_view(), name='exchange-list'),
    path('exchange/<int:pk>/update/', ExchangeProposalUpdateView.as_view(), name='exchange-update'),
]
