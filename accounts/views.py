from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse

from accounts.models import Token


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(f"{reverse('login')}?token={token.uid}")
    message_body = f"Use this lnk to log in:\n\n{url}"
    send_mail(
        "Your login link for Superlists",
        message_body,
        "noreply@superlists",
        [email],
    )
    messages.success(
        request, "Check your email, we've sent you a link you can use to log in."
    )
    return redirect("/")


def login(request):
    return redirect("home")
