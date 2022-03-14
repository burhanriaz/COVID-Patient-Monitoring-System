from django.contrib import admin
from django.urls import path, include

import Patient_Monitoring_System
from Patient import views
from django.contrib import admin

# admin.site.site_header = "Patient Monitoring System "
# admin.site.site_title = "Patient Monitoring System "
# admin.site.index_title = "Patient Monitoring System "

app_name = "Patient"

urlpatterns = [
    path("", views.home, name='patient'),
    path("Register/", views.Register, name='Register'),
    path("PatientRegister/", views.PatientRegister, name='PatientRegister'),
    path("Sensor/", views.Sensor, name='Sensor'),
    path("About/", views.About, name='About'),
    path("Graph/", views.Graph, name='Graph'),
    path("Login/", views.Login, name='Login'),
    path("Logout/", views.Logout, name='Logout'),
    path("Patientlist/", views.Patientlist, name='Patientlist'),
    path("forgotpassword/", views.forgotpassword, name='forgotpassword'),
    path("alertmessage/", views.alertmessage, name='alertmessage')

]
