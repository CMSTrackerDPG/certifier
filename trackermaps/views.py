import re
import logging
import paramiko
import subprocess

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('{}'.format(group_name), {
        'type': 'channel_message',
        'message': message
    })


def run_tracker_maps(run_type: str, run_number_list: list):
    """
    Function that connects to vocms066 using the env-supplied username/password
    and executes the script to generate specific tracker maps.
    """
    tracker_maps_command = f"cd /data/users/event_display/ShiftRun3/TkMapGeneration/CMS* &&"\
        " bash /data/users/event_display/ShiftRun3/TkMapGeneration/tkmapsFromCertHelper.sh"\
        f" {str(run_type)} {str(run_number_list)}"
    logger.debug(tracker_maps_command)
    return True
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # logger.debug("printing django secrets", settings.DJANGO_SECRET_ACC,
    # settings.DJANGO_SECRET_PASS)

    ssh.connect("vocms066",
                username=settings.DJANGO_SECRET_ACC,
                password=settings.DJANGO_SECRET_PASS)
    logger.debug(f"Executing '{tracker_maps_command}'")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(tracker_maps_command,
                                                         get_pty=True)

    for line in iter(ssh_stdout.readline, ""):
        send_channel_message("output_group", line)
    send_channel_message("output_group", "GENERATION ENDED\n")

    # This blocks until the process has exited
    exit_status = ssh_stdout.channel.recv_exit_status()

    if exit_status:
        logger.warning("Remote process exited with status {exit_status}")
        return False
    logger.info("Remote process terminated with no errors")
    return True


def maps(request):
    """
    View for the trackermaps/ url
    """
    context = {}

    if request.method == 'GET':
        return render(request, "trackermaps/trackermaps.html")

    # is_ajax has been deprecated
    # https://stackoverflow.com/questions/63629935/django-3-1-and-is-ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        run_type = request.POST.get("type", None)
        runs_list = request.POST.get("list", None)
        logger.info(
            f"Got trackermaps generation request for {run_type}: {runs_list}")
        if runs_list:
            try:
                runs_list = list(
                    map(
                        int,
                        re.split(
                            " , | ,|, |,| ",
                            re.sub(r'\s+', ' ', runs_list).lstrip().rstrip())))
                logger.debug(f"Parsed runs list: {runs_list}")
            except ValueError:
                context = {
                    "message":
                    "Run list should contain only numbers of runs separated by comma or space"
                }
                return JsonResponse(context, status=400)
            except Exception as e:
                context = {"message": repr(e)}
                return JsonResponse(context, status=500)

        run_tracker_maps(run_type, runs_list)

    return render(request, "trackermaps/trackermaps.html")
