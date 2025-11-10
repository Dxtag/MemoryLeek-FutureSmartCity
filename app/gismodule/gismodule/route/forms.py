from django import forms
from django.conf import settings
from .models import JoinPassengerRoute, PassengerRoute, TransportRoute, JoinTransportRoute
from django.forms import DateTimeField, DateTimeInput,IntegerField, HiddenInput
from django.db import models
from django.apps import apps

class PassengerRouteForm(forms.ModelForm):
    class Meta:
        model = PassengerRoute
        exclude=("owner",)
        widgets={
            "start_date":DateTimeInput(attrs={"type":"datetime-local"}),
            "geom":HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        _owner = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        app_label, model_name = settings.ROUTE_CAR_MODEL.split(".")
        car=apps.get_model(app_label, model_name)
        self.fields['car'].queryset =car.objects.filter(owner=_owner)

class TransportRouteForm(forms.ModelForm):
    class Meta:
        model = TransportRoute
        exclude=("owner",)
        widgets={
            "start_date":DateTimeInput(attrs={"type":"datetime-local"}),
            "geom":HiddenInput()
        }

    def __init__(self, *args, **kwargs) -> None:
        _owner = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        app_label, model_name = settings.ROUTE_CAR_MODEL.split(".")
        car=apps.get_model(app_label, model_name)
        self.fields['car'].queryset=car.objects.filter(owner=_owner)

class TransportJoinRouteForm(forms.ModelForm):
    class Meta:
        model = JoinTransportRoute
        exclude=("route","created", "creator")
        widgets={
            "start":HiddenInput(),
            "end":HiddenInput(),
            "start_time":DateTimeInput(attrs={"type":"datetime-local"})
        }

class PassengerJoinRouteForm(forms.ModelForm):
        class Meta:
            model = JoinPassengerRoute
            exclude=("route","created", "creator")
            widgets={
                "start":HiddenInput(),
                "end":HiddenInput(),
                "start_time":DateTimeInput(attrs={"type":"datetime-local"})
            }
