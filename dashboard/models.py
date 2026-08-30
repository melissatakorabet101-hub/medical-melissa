from django.db import models

from django.db import models

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="En attente")

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time}"


class Patient(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="En attente")

    def __str__(self):
        return self.name

class Invoice(models.Model):
    patient = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=50, default="Versé")

    def __str__(self):
        return f"Facture {self.id} - {self.patient}"


class MedicalRecord(models.Model):
    patient = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    last_visit = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Dossier médical - {self.patient}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
