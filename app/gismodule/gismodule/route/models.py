from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.gis.db.models import PointField, LineStringField
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

class PassengerRoute(Route):
    max_people = models.IntegerField(_("Max number of passengers"))
    description = models.TextField(_("Description"))

class JoinTransportRoute(models.Model):
    start = PointField(verbose_name=_("Start"))
    end = PointField(verbose_name=_("Start"))
    route = models.ForeignKey(TransportRoute, verbose_name=_("Joined route"), 
                              related_name="joined_transport_route", on_delete=models.CASCADE, null=True, blank=True)
    weight = models.IntegerField(_("weight (kg)"))
    width = models.IntegerField(_("width (cm)"))
    height = models.IntegerField(_("height (cm)"))
    depth = models.IntegerField(_("depth (cm)"))
    created= models.DateTimeField(_("Created"), auto_now_add=True)