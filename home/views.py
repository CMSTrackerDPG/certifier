from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "home/home.html")


def cablingmap(request):
    return render(request, "home/cablingmap.html")
