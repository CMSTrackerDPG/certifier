from django.shortcuts import render

# Create your views here.

from oms.utils import retrieve_run
from .forms import CertifyForm

def index(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)

    from django.shortcuts import redirect

    if run_number and reco:
        response = redirect("/certify/{}/{}".format(run_number, reco))
        return response

    return render(request, "certifier/index.html")


def certify(request, run_number, reco):
    try:
        run = retrieve_run(run_number)
    except IndexError:
        context = {"message": "Run {} does not exist".format(run_number)}
        return render(request, "certifier/404.html", context)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CertifyForm(request.POST)
        # check whether it's valid:
        print(form.errors.as_text())
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, "home/home.html")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CertifyForm()

    context = {"run_number": run_number, "reco": reco, "run": run, "form": form}

    return render(request, "certifier/certify.html", context)
