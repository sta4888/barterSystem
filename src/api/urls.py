from django.urls import path

from api.views import CategoryListAPI, AdListAPI, AdDetailAPI, ExchangeProposalListAPI, ExchangeProposalDetailAPI

app_name = "ads"

urlpatterns = [
    # API пути
    path('categories/', CategoryListAPI.as_view(), name='api-categories'),
    path('ads/', AdListAPI.as_view(), name='api-ads'),
    path('ads/<int:pk>/', AdDetailAPI.as_view(), name='api-ad-detail'),
    path('exchange-proposals/', ExchangeProposalListAPI.as_view(), name='api-exchange-list'),
    path('exchange-proposals/<int:pk>/', ExchangeProposalDetailAPI.as_view(), name='api-exchange-detail'),
]
