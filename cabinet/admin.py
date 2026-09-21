from django.contrib import admin
from .models import Patient, Dentiste, Rendezvous

admin.site.register(Patient)
admin.site.register(Dentiste)
admin.site.register(Rendezvous)

