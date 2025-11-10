from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView, View,FormView,CreateView
from .forms import PassengerJoinRouteForm, PassengerRouteForm, TransportJoinRouteForm, TransportRouteForm
from .models import JoinPassengerRoute, PassengerRoute, TransportRoute,JoinTransportRoute
from django.urls import reverse
from django.shortcuts import redirect
from typing import TYPE_CHECKING
from django.contrib.gis.geos import GEOSGeometry, Point
if TYPE_CHECKING:
    from .forms import PassengerRoute, TransportRouteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, F, Q


class IndexView(LoginRequiredMixin,TemplateView):
    template_name="route/index.html"


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
        form.geom = GEOSGeometry(self.request.POST.get("geom"))
        m = form.save()
        m.owner = self.request.user
        m.save()
        return super().form_valid(form)

class PassengerRouteJoinView(LoginRequiredMixin,View):

    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="route/form_join.html", context={"form":PassengerJoinRouteForm(), "title":"Join passenger route"})

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        form = PassengerJoinRouteForm(request.POST)
        if form.is_valid():
            m=form.save()
            m.creator = request.user
            m.save()
            messages.add_message(request, messages.INFO, _(f"Successfuly created route_to_join object pk={m.pk}"))
            return redirect("route:passenger_join_detail",pk=m.pk)
        else:
            return render(request, template_name="route/form_join.html", context={"form": form, "title":"Join passenger route"})


class PassengerRouteJoinFindView(LoginRequiredMixin,View):
    def get_possible_routes(self,route_join:JoinTransportRoute):
        potential_routes = PassengerRoute.objects.filter(
            geom__distance_lte=(route_join.start,settings.MAX_TRANSPORT_ROUTE_OFF_DISTANCE)).filter(
            geom__distance_lte=(route_join.end,settings.MAX_TRANSPORT_ROUTE_OFF_DISTANCE),
            start_date__gte=route_join.start_time
            )
        # Czy w dobrym kierunku
        correct_routes = []
        for r in potential_routes:
            start_line = Point(*r.geom.coords[0])
            good_direction = route_join.start.distance(start_line) < route_join.end.distance(start_line)
            free_seat = r.joined_passenger_route.count() < r.max_people
            if good_direction and free_seat:
                correct_routes.append(r)
        return correct_routes
                
    def get(self,request:HttpRequest, pk:int, *args, **kwargs):
        route_join = get_object_or_404(JoinPassengerRoute, pk=pk)
        routes = self.get_possible_routes(route_join)
        return render(request, template_name="route/routes_list_passenger.html", context={"routes":routes,"route_join":route_join})
    
    def post(self,request:HttpRequest, pk:int, *args, **kwargs):
        route_join = get_object_or_404(JoinPassengerRoute, pk=pk)
        route_to_join = get_object_or_404(PassengerRoute,pk=request.POST["route"])
        route_join.route=route_to_join
        route_join.save()
        messages.add_message(request, messages.INFO, _(f"Joined route {route_to_join.pk}"))
        return render(request, template_name="route/routes_list_passenger.html", context={"route_join":route_join})

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
        form.geom = GEOSGeometry(self.request.POST.get("geom"))
        m = form.save()
        m.owner = self.request.user
        m.save()
        return super().form_valid(form)

class TransportRouteJoinView(LoginRequiredMixin,View):

    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="route/form_join.html", context={"form":TransportJoinRouteForm(), "title":"Join transport route"})

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
        form = TransportJoinRouteForm(request.POST)
        if form.is_valid():
            m=form.save()
            m.creator = request.user
            m.save()
            messages.add_message(request, messages.INFO, _(f"Successfuly created route_to_join object pk={m.pk}"))
            return redirect("route:transport_join_detail",pk=m.pk)
        else:
            return render(request, template_name="route/form_join.html", context={"form": form, "title":"Join transport route"})


class TransportRouteJoinFindView(LoginRequiredMixin,View):
    def get_possible_routes(self,route_join:JoinTransportRoute):
        potential_routes = TransportRoute.objects.filter(
            geom__distance_lte=(route_join.start,settings.MAX_TRANSPORT_ROUTE_OFF_DISTANCE)).filter(
            geom__distance_lte=(route_join.end,settings.MAX_TRANSPORT_ROUTE_OFF_DISTANCE),
            max_weight__gte=route_join.weight,
            max_width__gte=route_join.width,
            max_height__gte=route_join.height,
            max_depth__gte=route_join.depth,
            start_date__gte=route_join.start_time
            )
        correct_routes=[]
        # Czy w dobrym kierunku
        for r in potential_routes:
            start_line = Point(*r.geom.coords[0])
            if route_join.start.distance(start_line) < route_join.end.distance(start_line):
                correct_routes.append(r)
        return correct_routes
                
    def get(self,request:HttpRequest, pk:int, *args, **kwargs):
        route_join = get_object_or_404(JoinTransportRoute, pk=pk)
        routes = self.get_possible_routes(route_join)
        return render(request, template_name="route/routes_list_transport.html", context={"routes":routes,"route_join":route_join})
    
    def post(self,request:HttpRequest, pk:int, *args, **kwargs):
        route_join:JoinTransportRoute = get_object_or_404(JoinTransportRoute, pk=pk)
        route_to_join:TransportRoute = get_object_or_404(TransportRoute,pk=request.POST["route"])
        route_join.route=route_to_join
        route_join.save()
        messages.add_message(request, messages.INFO, _(f"Joined route {route_to_join.pk}"))
        return render(request, template_name="route/routes_list_transport.html", context={"route_join":route_join})
    

class TransportRouteDetailView(DetailView):
    model = TransportRoute
    template_name = "route/transportroute_detail.html"
    context_object_name = "r"


class PassengerRouteDetailView(DetailView):
    model = PassengerRoute
    template_name = "route/passengerroute_detail.html"
    context_object_name = "r"

class StatisticsView(View):
    def prepare_data(self):
        t = TransportRoute.objects.all()
        p = PassengerRoute.objects.all()
        data = []
        for i in t:
            data.append(["transport",str(i.start_date),i.geom.json])
        for i in p:
            data.append(["passenger",str(i.start_date),i.geom.json])
        return data

    def get(self,request) -> None:
        return render(request, template_name="route/statistics.html", context={"statistics":self.prepare_data()})