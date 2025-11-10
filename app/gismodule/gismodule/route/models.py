from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.gis.db.models import PointField, LineStringField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Route(models.Model):
    class Meta:
        abstract=True
    # created_transportroutes
    owner = models.ForeignKey(get_user_model(), verbose_name=_("Route owner"), 
                              on_delete=models.CASCADE, related_name="created_%(class)s", null=True, blank=True)
    # n_transportroutes
    car = models.ForeignKey(settings.ROUTE_CAR_MODEL, verbose_name=_("Route car"), on_delete=models.CASCADE, 
                            related_name="%(class)s", null=True, blank=True)
    
    geom = LineStringField(_("Route"))
    start_date = models.DateTimeField(_("Start time"), auto_now=False, auto_now_add=False)


class TransportRoute(Route):
    max_weight = models.IntegerField(_("Max weight (kg)"))
    max_width = models.IntegerField(_("Max width (cm)"))
    max_height = models.IntegerField(_("Max height (cm)"))
    max_depth = models.IntegerField(_("Max depth (cm)"))
    description = models.TextField(_("Description"))
    def get_absolute_url(self):
        return reverse("route:transportroute_detail", args=[self.pk])

class PassengerRoute(Route):
    max_people = models.IntegerField(_("Max number of passengers"))
    description = models.TextField(_("Description"))
    def get_absolute_url(self):
        return reverse("route:passengerroute_detail", args=[self.pk])

class JoinPassengerRoute(models.Model):
    creator = models.ForeignKey(get_user_model(), verbose_name=_("join route passenger"), 
                              on_delete=models.CASCADE, related_name="joined_%(class)s", null=True, blank=True)
    start = PointField(verbose_name=_("Start"))
    end = PointField(verbose_name=_("Start"))
    route = models.ForeignKey(PassengerRoute, verbose_name=_("Joined route"), 
                              related_name="joined_passenger_route", on_delete=models.CASCADE, null=True, blank=True)
    start_time=models.DateTimeField(_("start time"))
    created=models.DateTimeField(_("Created"), auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("route:passenger_join_detail", args=[self.pk])

    

class JoinTransportRoute(models.Model):
    creator = models.ForeignKey(get_user_model(), verbose_name=_("join route creator"), 
                              on_delete=models.CASCADE, related_name="joined_%(class)s", null=True, blank=True)
    start = PointField(verbose_name=_("Start"))
    end = PointField(verbose_name=_("Start"))
    route = models.ForeignKey(TransportRoute, verbose_name=_("Joined route"), 
                              related_name="joined_transport_route", on_delete=models.CASCADE, null=True, blank=True)
    weight = models.IntegerField(_("weight (kg)"))
    width = models.IntegerField(_("width (cm)"))
    height = models.IntegerField(_("height (cm)"))
    depth = models.IntegerField(_("depth (cm)"))
    start_time=models.DateTimeField(_("start time"))
    created= models.DateTimeField(_("Created"), auto_now_add=True)

    def get_absolute_url(self):
        return reverse("route:transport_join_detail", args=[self.pk])