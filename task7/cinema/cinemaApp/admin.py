from django.contrib import admin
from cinemaApp.models import Projection, Ticket
# Register your models here.

admin.site.register(Ticket)
admin.site.register(Projection)