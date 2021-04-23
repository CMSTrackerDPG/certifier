from django.shortcuts import render

# Create your views here.

def mlplayground(request):
    return render(request, "mlplayground/mlplayground.html")
