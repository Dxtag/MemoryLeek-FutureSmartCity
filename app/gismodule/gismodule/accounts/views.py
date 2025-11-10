from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class ProfileView(LoginRequiredMixin, View):
    def get(self, request:HttpRequest) -> HttpResponse:
        user = request.user
        return render(request, "accounts/profile.html", {
            "transportroutes":user.created_transportroute.all(),
            "passengerroutes":user.created_passengerroute.all(),
            "joinpassengerroutes":user.joined_joinpassengerroute.all(),
            "jointransportroutes":user.joined_jointransportroute.all(),

        })
    


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("accounts:profile")  