from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment, Patient, Invoice, MedicalRecord, ContactMessage
from .config import (
    CLINIC_NAME,
    DOCTOR_NAME,
    CLINIC_PHONE,
    CLINIC_EMAIL,
    CLINIC_LOGO,
)

from datetime import date as date_type
from datetime import time as time_type

import json

@login_required(login_url='/login/')
def home(request):

    appointments = Appointment.objects.all().order_by('-date', '-time')

    return render(
        request,
        'dashboard/index.html',
        {
            'appointments': appointments,
            'clinic_name': CLINIC_NAME,
            'doctor_name': DOCTOR_NAME,
            'clinic_phone': CLINIC_PHONE,
            'clinic_email': CLINIC_EMAIL,
            'clinic_logo': CLINIC_LOGO,
        }
    )


# =========================================================
# API RENDEZ-VOUS
# =========================================================

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def appointments_api(request):

    # GET — récupérer les rendez-vous
    if request.method == "GET":
        appointments = Appointment.objects.all().order_by("-date", "-time")

        data = [
            {
                "id": appointment.id,
                "patient_name": appointment.patient_name,
                "date": appointment.date.isoformat(),
                "time": appointment.time.strftime("%H:%M"),
                "reason": appointment.reason,
                "status": appointment.status,
            }
            for appointment in appointments
        ]

        return JsonResponse(data, safe=False)

    # POST — ajouter un rendez-vous
    if request.method == "POST":
        data = json.loads(request.body)

        appointment = Appointment.objects.create(
            patient_name=data.get("patient_name", ""),
            date=date_type.fromisoformat(data.get("date")),
            time=time_type.fromisoformat(
                data.get("time")
            ).replace(tzinfo=None),
            reason=data.get("reason", ""),
            status=data.get("status", "En attente"),
        )

        return JsonResponse({
            "id": appointment.id,
            "patient_name": appointment.patient_name,
            "date": appointment.date.isoformat(),
            "time": appointment.time.strftime("%H:%M"),
            "reason": appointment.reason,
            "status": appointment.status,
        }, status=201)

    # PUT — modifier un rendez-vous
    if request.method == "PUT":
        data = json.loads(request.body)

        print("DONNEES PUT :", data)

        appointment_id = data.get("id")

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return JsonResponse(
                {"error": "Rendez-vous introuvable."},
                status=404
            )

        if data.get("patient_name") is not None:
            appointment.patient_name = data.get("patient_name")

        if data.get("date"):
            appointment.date = date_type.fromisoformat(
                data.get("date")
            )

        if data.get("time"):
            appointment.time = time_type.fromisoformat(
                data.get("time")
            ).replace(tzinfo=None)

        if data.get("reason") is not None:
            appointment.reason = data.get("reason")

        if data.get("status") is not None:
            appointment.status = data.get("status")

        appointment.save()

        return JsonResponse({
            "id": appointment.id,
            "patient_name": appointment.patient_name,
            "date": appointment.date.isoformat(),
            "time": appointment.time.strftime("%H:%M"),
            "reason": appointment.reason,
            "status": appointment.status,
        })

    # DELETE — supprimer un rendez-vous
    if request.method == "DELETE":
        data = json.loads(request.body)

        appointment_id = data.get("id")

        print("ID SUPPRESSION :", appointment_id)

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return JsonResponse(
                {"error": "Rendez-vous introuvable."},
                status=404
            )

        appointment.delete()

        return JsonResponse({
            "success": True,
            "message": "Rendez-vous supprimé avec succès."
        })


# =========================================================
# API PATIENTS
# =========================================================

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def patients_api(request):

    # GET — récupérer les patients
    if request.method == "GET":
        patients = Patient.objects.all().order_by("-id")

        data = [
            {
                "id": patient.id,
                "name": patient.name,
                "gender": patient.gender,
                "birthDate": (
                    patient.birth_date.isoformat()
                    if patient.birth_date
                    else ""
                ),
                "time": (
                    patient.time.strftime("%H:%M")
                    if patient.time
                    else ""
                ),
                "reason": patient.reason,
                "status": patient.status,
            }
            for patient in patients
        ]

        return JsonResponse(data, safe=False)

    # POST — ajouter un patient
    if request.method == "POST":
        data = json.loads(request.body)

        patient = Patient.objects.create(
            name=data.get("name", ""),
            gender=data.get("gender", ""),
            birth_date=(
                date_type.fromisoformat(data["birthDate"])
                if data.get("birthDate")
                else None
            ),
            time=(
                time_type.fromisoformat(data["time"]).replace(tzinfo=None)
                if data.get("time")
                else None
            ),
            reason=data.get("reason", ""),
            status=data.get("status", "En attente"),
        )

        return JsonResponse({
            "id": patient.id,
            "name": patient.name,
            "gender": patient.gender,
            "birthDate": (
                patient.birth_date.isoformat()
                if patient.birth_date
                else ""
            ),
            "time": (
                patient.time.strftime("%H:%M")
                if patient.time
                else ""
            ),
            "reason": patient.reason,
            "status": patient.status,
        }, status=201)

    # PUT — modifier un patient
    if request.method == "PUT":
        data = json.loads(request.body)

        patient_id = data.get("id")

        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return JsonResponse(
                {"error": "Patient introuvable."},
                status=404
            )

        if data.get("name") is not None:
            patient.name = data.get("name")

        if data.get("gender") is not None:
            patient.gender = data.get("gender")

        if data.get("birthDate"):
            patient.birth_date = date_type.fromisoformat(
                data.get("birthDate")
            )

        if data.get("time"):
            patient.time = time_type.fromisoformat(
                data.get("time")
            ).replace(tzinfo=None)

        if data.get("reason") is not None:
            patient.reason = data.get("reason")

        if data.get("status") is not None:
            patient.status = data.get("status")

        patient.save()

        return JsonResponse({
            "id": patient.id,
            "name": patient.name,
            "gender": patient.gender,
            "birthDate": (
                patient.birth_date.isoformat()
                if patient.birth_date
                else ""
            ),
            "time": (
                patient.time.strftime("%H:%M")
                if patient.time
                else ""
            ),
            "reason": patient.reason,
            "status": patient.status,
        })

    # DELETE — supprimer un patient
    if request.method == "DELETE":
        data = json.loads(request.body)

        patient_id = data.get("id")

        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return JsonResponse(
                {"error": "Patient introuvable."},
                status=404
            )

        patient.delete()

        return JsonResponse({
            "success": True,
            "message": "Patient supprimé avec succès."
        })

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def invoices_api(request):

    # GET — récupérer les factures
    if request.method == "GET":
        invoices = Invoice.objects.all().order_by("-id")

        data = [
            {
                "id": invoice.id,
                "patient": invoice.patient,
                "amount": float(invoice.amount),
                "paid": float(invoice.paid),
                "dueDate": invoice.due_date.isoformat(),
                "status": invoice.status,
            }
            for invoice in invoices
        ]

        return JsonResponse(data, safe=False)

    # POST — ajouter une facture
    if request.method == "POST":
        data = json.loads(request.body)

        invoice = Invoice.objects.create(
            patient=data.get("patient", ""),
            amount=data.get("amount", 0),
            paid=data.get("paid", 0),
            due_date=date_type.fromisoformat(data.get("dueDate")),
            status=data.get("status", "Versé"),
        )

        return JsonResponse({
            "id": invoice.id,
            "patient": invoice.patient,
            "amount": float(invoice.amount),
            "paid": float(invoice.paid),
            "dueDate": invoice.due_date.isoformat(),
            "status": invoice.status,
        }, status=201)

    # PUT — modifier une facture
    if request.method == "PUT":
        data = json.loads(request.body)
        print("DONNEES FACTURE PUT :", data)
        invoice_id = data.get("id")

        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return JsonResponse(
                {"error": "Facture introuvable."},
                status=404
            )

        if data.get("patient") is not None:
            invoice.patient = data.get("patient")

        if data.get("amount") is not None:
            invoice.amount = data.get("amount")

        if data.get("paid") is not None:
            invoice.paid = data.get("paid")

        if data.get("dueDate"):
            invoice.due_date = date_type.fromisoformat(
                data.get("dueDate")
            )

        if data.get("status") is not None:
            invoice.status = data.get("status")

        invoice.save()

        return JsonResponse({
            "id": invoice.id,
            "patient": invoice.patient,
            "amount": float(invoice.amount),
            "paid": float(invoice.paid),
            "dueDate": invoice.due_date.isoformat(),
            "status": invoice.status,
        })

    # DELETE — supprimer une facture
    if request.method == "DELETE":
        data = json.loads(request.body)

        invoice_id = data.get("id")

        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return JsonResponse(
                {"error": "Facture introuvable."},
                status=404
            )

        invoice.delete()

        return JsonResponse({
            "success": True,
            "message": "Facture supprimée avec succès."
        })


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def medical_records_api(request):

    # GET — récupérer les dossiers
    if request.method == "GET":
        records = MedicalRecord.objects.all().order_by("-id")

        data = [
            {
                "id": record.id,
                "patient": record.patient,
                "birthDate": record.birth_date.isoformat()
                if record.birth_date else "",
                "diagnosis": record.diagnosis,
                "treatment": record.treatment,
                "lastVisit": record.last_visit.isoformat()
                if record.last_visit else "",
                "notes": record.notes,
            }
            for record in records
        ]

        return JsonResponse(data, safe=False)

    # POST — créer un dossier
    if request.method == "POST":
        data = json.loads(request.body)

        record = MedicalRecord.objects.create(
            patient=data.get("patient", ""),
            birth_date=date_type.fromisoformat(data["birthDate"])
            if data.get("birthDate") else None,
            diagnosis=data.get("diagnosis", ""),
            treatment=data.get("treatment", ""),
            last_visit=date_type.fromisoformat(data["lastVisit"])
            if data.get("lastVisit") else None,
            notes=data.get("notes", ""),
        )

        return JsonResponse({
            "id": record.id,
            "patient": record.patient,
            "birthDate": record.birth_date.isoformat()
            if record.birth_date else "",
            "diagnosis": record.diagnosis,
            "treatment": record.treatment,
            "lastVisit": record.last_visit.isoformat()
            if record.last_visit else "",
            "notes": record.notes,
        }, status=201)

    # PUT — modifier un dossier
    if request.method == "PUT":
        data = json.loads(request.body)

        record_id = data.get("id")

        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return JsonResponse(
                {"error": "Dossier médical introuvable."},
                status=404
            )

        if data.get("patient") is not None:
            record.patient = data.get("patient")

        if data.get("birthDate"):
            record.birth_date = date_type.fromisoformat(
                data.get("birthDate")
            )

        if data.get("diagnosis") is not None:
            record.diagnosis = data.get("diagnosis")

        if data.get("treatment") is not None:
            record.treatment = data.get("treatment")

        if data.get("lastVisit"):
            record.last_visit = date_type.fromisoformat(
                data.get("lastVisit")
            )

        if data.get("notes") is not None:
            record.notes = data.get("notes")

        record.save()

        return JsonResponse({
            "id": record.id,
            "patient": record.patient,
            "birthDate": record.birth_date.isoformat()
            if record.birth_date else "",
            "diagnosis": record.diagnosis,
            "treatment": record.treatment,
            "lastVisit": record.last_visit.isoformat()
            if record.last_visit else "",
            "notes": record.notes,
        })

    # DELETE — supprimer un dossier
    if request.method == "DELETE":
        data = json.loads(request.body)

        record_id = data.get("id")

        try:
            record = MedicalRecord.objects.get(id=record_id)
        except MedicalRecord.DoesNotExist:
            return JsonResponse(
                {"error": "Dossier médical introuvable."},
                status=404
            )

        record.delete()

        return JsonResponse({
            "success": True,
            "message": "Dossier médical supprimé avec succès."
        })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def contact_api(request):

    # GET — récupérer les messages
    if request.method == "GET":
        messages = ContactMessage.objects.all().order_by("-id")

        data = [
            {
                "id": message.id,
                "name": message.name,
                "email": message.email,
                "message": message.message,
                "date": message.date.isoformat(),
            }
            for message in messages
        ]

        return JsonResponse(data, safe=False)

    # POST — envoyer un message
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message_text = data.get("message", "").strip()

        if not name or not message_text:
            return JsonResponse(
                {"error": "Le nom et le message sont obligatoires."},
                status=400
            )

        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text,
        )

        return JsonResponse(
            {
                "id": contact_message.id,
                "name": contact_message.name,
                "email": contact_message.email,
                "message": contact_message.message,
                "date": contact_message.date.isoformat(),
            },
            status=201
        )
