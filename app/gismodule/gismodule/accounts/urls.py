from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import ProfileView

app_name = "accounts"

urlpatterns = [
    path("profile", ProfileView.as_view(), name="profile"),
]
