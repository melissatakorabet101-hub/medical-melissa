"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard.views import (
    home,
    appointments_api,
    patients_api,
    invoices_api,
    medical_records_api,
    contact_api,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='dashboard/registration/login.html'
    ),
    name='login'
),
    path(
    'logout/',
    auth_views.LogoutView.as_view(),
    name='logout'
),
    path('', home, name='home'),

    path(
        'api/appointments/',
        appointments_api,
        name='appointments_api'
    ),

    path(
        'api/patients/',
        patients_api,
        name='patients_api'
    ),

    path(
        'api/invoices/',
        invoices_api,
        name='invoices_api'
    ),

    path(
        'api/medical-records/',
        medical_records_api,
        name='medical_records_api'
    ),

    path('api/contact/', contact_api, name='contact_api'),
]

