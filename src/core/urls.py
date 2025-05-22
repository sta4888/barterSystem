from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("api/", include("api.urls", namespace="api")),
    path("", include("ads.urls", namespace="ads")),

    # Схема OpenAPI в JSON
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI (по желанию)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
