from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

@login_required
def logout_view(request):
    """
    Logout current user (also from CERN)
    """
    logout(request)
    callback_url = "https://login.cern.ch/adfs/ls/?wa=wsignout1.0&ReturnUrl="
    callback_url += "http%3A//"
    callback_url += request.META["HTTP_HOST"]
    callback_url += reverse("users:logout_status")
    return HttpResponseRedirect(callback_url)

def logout_status(request):
    """
    Simple status page which should help determining
    if the logout was successful or not
    """
    logout_successful = not request.user.is_authenticated
    return render(
        request,
        "users/logout_status.html",
        {"logout_successful": logout_successful},
    )
