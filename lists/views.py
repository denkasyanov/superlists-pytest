from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls.base import resolve


def home_page(request: HttpRequest) -> HttpResponse:
    # if request.method == "POST":
    #     return render(request, "home.html", {"new_item_text": request.POST["item_text"]})
    return render(
        request, "home.html", {"new_item_text": request.POST.get("item_text", "")}
    )
