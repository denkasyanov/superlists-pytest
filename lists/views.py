from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<html><title>To-Do lists</title></html>")
