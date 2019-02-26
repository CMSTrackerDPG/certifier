from django.shortcuts import render


# Create your views here.


def index(request):
    run_number = request.GET.get("run_number", None)
    reco = request.GET.get("reco", None)

    from django.shortcuts import redirect

    if run_number and reco:
        response = redirect('/certify/{}/{}'.format(run_number, reco))
        return response

    return render(request, 'crtfr/index.html')


def certify(request, run_number, reco):
    context = {'run_number': run_number, 'reco': reco}
    return render(request, 'crtfr/certify.html', context)


def analyse(request, run_number, reco):
    context = {'run_number': run_number, 'reco': reco}
    return render(request, 'crtfr/analyse.html', context)
