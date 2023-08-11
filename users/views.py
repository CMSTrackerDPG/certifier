import urllib.parse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.http import HttpResponseRedirect


@login_required
def logout_view(request):
    """
    Logout current user (also from CERN)
    """
    logout(request)
    callback_url = "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/logout?post_logout_redirect_uri="
    redirect_url = urllib.parse.quote(
        f"https://{request.META['HTTP_HOST']}{reverse('users:logout_status')}"
    )
    return HttpResponseRedirect(callback_url + redirect_url)


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
