from django.contrib import admin
from .models import *

admin.site.register(Tickets)
admin.site.register(TicketPrice)
admin.site.register(TicketLog)