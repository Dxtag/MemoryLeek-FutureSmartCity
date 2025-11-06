from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View,FormView,CreateView
from .forms import PassengerRouteForm, TransportJoinRouteForm, TransportRouteForm
from .models import PassengerRoute, TransportRoute, settings
from django.urls import reverse
from typing import TYPE_CHECKING
from django.contrib.gis.geos import GEOSGeometry, Point
if TYPE_CHECKING:
    from .forms import PassengerRoute, TransportRouteForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PassengerRouteCreateView(LoginRequiredMixin,FormView):
    form_class=PassengerRouteForm
    model=PassengerRoute
    template_name="route/form.html"
    success_url= settings.CREATE_ROUTE_REDIRECT_URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form:"PassengerRoute") -> HttpResponse:
        form.owner = self.request.user
        form.geom = GEOSGeometry(self.request.POST.get("geom"))
        form.save()
        return super().form_valid(form)
    

class TransportRouteCreateView(LoginRequiredMixin,FormView):
    form_class=TransportRouteForm
    model=TransportRoute
    template_name="route/form.html"
    success_url= settings.CREATE_ROUTE_REDIRECT_URL
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form:"TransportRouteForm") -> HttpResponse:
        form.owner = self.request.user
        form.geom = GEOSGeometry(self.request.POST.get("geom"))
        form.save()
        return super().form_valid(form)

class IndexView(LoginRequiredMixin,TemplateView):
    template_name="route/index.html"


class TransportRouteJoinView(LoginRequiredMixin,View):
    
    def get_possible_routes(self,start:Point,end:Point):
        pass

    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="route/form_join.html", context={"form":TransportJoinRouteForm()})

    def post(self, request:HttpRequest, *args, **kwargs):
        form = TransportJoinRouteForm(request)
        if form.is_valid():
            return render(request, "route/routes_list.html", {"form": form})
        else:
            return render(request, template_name="route/form_join.html", context={"form": form})
    
# class TransportRouteCreateView(LoginRequiredMixin,View):
#     form_class=TransportRouteForm
#     model=TransportRoute
#     template_name="route/form.html"
#     success_url= settings.CREATE_ROUTE_REDIRECT_URL
    
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
    
#     def form_valid(self, form:"TransportRouteForm") -> HttpResponse:
#         form.owner = self.request.user
#         form.geom = GEOSGeometry(self.request.POST.get("geom"))
#         form.save()
#         return super().form_valid(form)