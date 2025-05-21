from django.urls import path

from ads.views import index

app_name = 'ads'

urlpatterns = [
    path("main/", index, name="home"),
]
