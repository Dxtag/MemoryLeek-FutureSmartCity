from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView, View,FormView,CreateView
from .forms import PassengerRouteForm, TransportJoinRouteForm, TransportRouteForm
from .models import PassengerRoute, TransportRoute,JoinTransportRoute
from django.urls import reverse
from django.shortcuts import redirect
from typing import TYPE_CHECKING
from django.contrib.gis.geos import GEOSGeometry, Point
if TYPE_CHECKING:
    from .forms import PassengerRoute, TransportRouteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


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

    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="route/form_join.html", context={"form":TransportJoinRouteForm()})

    def post(self, request:HttpRequest, *args, **kwargs):
        form = TransportJoinRouteForm(request.POST)
        if form.is_valid():
            m=form.save(commit=True)
            return redirect("route:transport_join_detail",pk=m.pk)
        else:
            return render(request, template_name="route/form_join.html", context={"form": form})


class TransportRouteJoinFindView(LoginRequiredMixin,View):
    def get_possible_routes(self,start:Point,end:Point):
        potential_routes = TransportRoute.objects.filter(
            geom__distance_lte=(start,settings.MAX_TRANSPORT_ROUTE_OFF_DISTANCE)).filter(
            geom__distance_lte=(end,settings.MAX_TRANSPORT_ROUTE_OFF_DISTANCE))
        correct_routes=[]
        for r in potential_routes:
            start_line = Point(*r.geom.coords[0])
            if start.distance(start_line) < end.distance(start_line):
                correct_routes.append(r)
        return correct_routes
                
    def get(self,request:HttpRequest, pk:int, *args, **kwargs):
        route_join = get_object_or_404(JoinTransportRoute, pk=pk)
        routes = self.get_possible_routes(route_join.start, route_join.end)
        return render(request, template_name="route/routes_list.html", context={"routes":routes,"route_join":route_join})
    
    def post(self,request:HttpRequest, pk:int, *args, **kwargs):
        route_join = get_object_or_404(JoinTransportRoute, pk=pk)
        route_to_join = get_object_or_404(TransportRoute,request.POST["route"])
        routes = self.get_possible_routes(route_join.start, route_join.end)
        if route_join not in routes:
            return render(request, template_name="route/routes_list.html", context={"routes":routes, "route_join":route_join})
        route_join.route=route_to_join
        route_join.save()
        messages.add_message(request, messages.INFO, _(f"Joined route {route_to_join.pk}"))
        return redirect("route:index")

        
            
        

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