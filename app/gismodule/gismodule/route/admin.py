from django.contrib import admin
from . models import TransportRoute, PassengerRoute, JoinPassengerRoute, JoinTransportRoute


admin.site.register(TransportRoute)
admin.site.register(PassengerRoute)
admin.site.register(JoinPassengerRoute)
admin.site.register(JoinTransportRoute)