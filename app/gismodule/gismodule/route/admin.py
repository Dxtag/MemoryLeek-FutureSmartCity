from django.contrib import admin
from . models import TransportRoute, PassengerRoute


admin.site.register(TransportRoute)
admin.site.register(PassengerRoute)