import re
from django_tables2 import RequestConfig
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cernrequests.certs import CertificateNotFound
from urllib3.exceptions import ProtocolError
from openruns.models import OpenRuns
from openruns.utilities import get_range_of_open_runs, get_specific_open_runs
from tables.tables import OpenRunsTable


@login_required
def openruns(request):
    """
    View used to render the openruns.html page.

    Accepts GET (with or without parameters) and POST requests.
    """
    context = {}
    show_openruns = []
    if request.method == "GET":
        run_number = request.GET.get("run_number", None)
        reco = request.GET.get("reco", None)

        if run_number and reco:
            response = redirect("/certify/{}/{}".format(run_number, reco))
            return response

        if run_number:
            response = redirect("/certify/{}".format(run_number))
            return response

        # GET request without parameters
        today = timezone.now().strftime("%Y-%m-%d")

        show_openruns = OpenRuns.objects.filter(date_retrieved=today).order_by(
            "-run_number"
        )

    # Search for openruns
    elif request.method == "POST":

        min_run_number = request.POST.get("min", None)
        max_run_number = request.POST.get("max", None)

        runs_list = request.POST.get("list", None)

        runs_search_limit = 20

        if runs_list:
            try:
                runs_list = list(
                    map(
                        int,
                        re.split(
                            " , | ,|, |,| ",
                            re.sub(r"\s+", " ", runs_list).lstrip().rstrip(),
                        ),
                    )
                )
                if len(runs_list) >= runs_search_limit:
                    messages.warning(
                        request, f"Please search for less than {runs_search_limit} runs"
                    )
                else:
                    get_specific_open_runs(runs_list)
                    show_openruns = OpenRuns.objects.filter(
                        run_number__in=runs_list
                    ).order_by("-run_number")

            except ValueError:
                context = {
                    "message": "Run list should contain only numbers of runs separated by comma or space"
                }
                return render(request, "certifier/404.html", context)
            except CertificateNotFound as e:
                return HttpResponse(
                    "Incorrect configuration of RunRegistry certificates", status=503,
                )
            except ProtocolError as e:
                return HttpResponse(f"ProtocolError occurred: {e}", status=503)
            except ConnectionError as e:
                return HttpResponse(f"ConnectionError occurred: {e}", status=503)

        elif min_run_number and max_run_number:
            number_of_runs = int(max_run_number) - int(min_run_number)
            if number_of_runs >= runs_search_limit:
                messages.warning(
                    request, f"Please search for less than {runs_search_limit} runs"
                )
            else:
                try:
                    get_range_of_open_runs(min_run_number, max_run_number)
                    show_openruns = OpenRuns.objects.filter(
                        run_number__gte=min_run_number, run_number__lte=max_run_number
                    ).order_by("-run_number")

                # Missing certificate
                except CertificateNotFound as e:
                    return HttpResponse(
                        "Incorrect configuration of RunRegistry certificates",
                        status=503,
                    )
                except ProtocolError as e:
                    return HttpResponse(f"ProtocolError occurred: {e}", status=503)
                except ConnectionError as e:
                    return HttpResponse(f"ConnectionError occurred: {e}", status=503)

    # Add table, with list of openruns created depending on the filters
    openruns_table = OpenRunsTable(show_openruns)
    openruns_table.request = request
    RequestConfig(request).configure(openruns_table)
    context["openruns_table"] = openruns_table

    return render(request, "openruns/openruns.html", context)
