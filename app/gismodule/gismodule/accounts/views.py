from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, View):
    def get(self, request:HttpRequest) -> HttpResponse:
        user = request.user
        return render(request, "accounts/profile.html", {
            "transportroutes":user.created_transportroute.all(),
            "passengerroutes":user.created_passengerroute.all(),
            "joinpassengerroutes":user.joined_joinpassengerroute.all(),
            "jointransportroutes":user.joined_jointransportroute.all(),

        })