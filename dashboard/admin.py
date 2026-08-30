from django.contrib import admin
from django.contrib import admin
from .models import Appointment, Patient, Invoice, MedicalRecord, ContactMessage

admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Invoice)
admin.site.register(MedicalRecord)
admin.site.register(ContactMessage)