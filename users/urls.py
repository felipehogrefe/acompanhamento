from django.conf.urls import url
from django.urls import path, include

from users.views import register

app_name = 'users'
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
]
