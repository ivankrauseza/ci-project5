from django.urls import path
from . import views


urlpatterns = [
    path('about-us/', views.AboutUs, name='about'),
    path('contact-us/', views.ContactUs, name='contact'),
    path('terms-conditions/', views.TermsConditions, name='terms'),
    path('privacy-policy/', views.PrivacyPolicy, name='privacy'),
]
