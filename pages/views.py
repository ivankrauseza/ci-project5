from django.shortcuts import render


# About :
def AboutUs(request):
    return render(request, "about_us.html")


# Terms & Conditions :
def TermsConditions(request):
    return render(request, "terms_conditions.html")


# Contact Us :
def ContactUs(request):
    return render(request, "contact_us.html")


# Privacy Policy :
def PrivacyPolicy(request):
    return render(request, "privacy_policy.html")
