from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View


class AccountView(View):
    def get(request:HttpRequest) -> HttpResponse:
        return render(request, "account.html", {

        })