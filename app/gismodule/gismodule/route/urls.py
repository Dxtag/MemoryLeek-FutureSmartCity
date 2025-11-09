from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import PassengerRouteCreateView, TransportRouteCreateView, IndexView, TransportRouteJoinView,TransportRouteJoinFindView

app_name = "route"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("passenger", PassengerRouteCreateView.as_view(), name="passenger"),
    path("transport", TransportRouteCreateView.as_view(), name="transport"),
    path("transport/join/", TransportRouteJoinView.as_view(), name="transport_join"),
    path("transport/join/<pk>", TransportRouteJoinFindView.as_view(), name="transport_join_detail")
]
