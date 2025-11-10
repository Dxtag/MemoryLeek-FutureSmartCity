from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import PassengerRouteCreateView, PassengerRouteDetailView, TransportRouteCreateView, IndexView, TransportRouteDetailView, TransportRouteJoinView,TransportRouteJoinFindView, PassengerRouteJoinFindView, PassengerRouteJoinView

app_name = "route"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("passenger", PassengerRouteCreateView.as_view(), name="passenger"),
    path("passenger/join/", PassengerRouteJoinView.as_view(), name="passenger_join"),
    path("passenger/join/<pk>", PassengerRouteJoinFindView.as_view(), name="passenger_join_detail"),
    path("passenger/<int:pk>/", PassengerRouteDetailView.as_view(), name="passengerroute_detail"),

    path("transport", TransportRouteCreateView.as_view(), name="transport"),
    path("transport/join/", TransportRouteJoinView.as_view(), name="transport_join"),
    path("transport/join/<pk>", TransportRouteJoinFindView.as_view(), name="transport_join_detail"),
    path("transport/<int:pk>/", TransportRouteDetailView.as_view(), name="transportroute_detail")

    
]
