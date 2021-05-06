from django.shortcuts import render

# Create your views here.
def cablingmapHome(request):
    return render(request, "cablingmap/cablingmap.html")