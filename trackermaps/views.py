import subprocess
import re
import os
import paramiko
import logging
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

logger = logging.getLogger(__name__)


def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('{}'.format(group_name), {
        'type': 'channel_message',
        'message': message
    })


def run_tracker_maps(run_type, min_run_number, max_run_number):
    logger.info(f"Tracker maps for '{run_type}' runs with number"
                f"{min_run_number} to {max_run_number}")
    #tracker_maps_command = "python /home/cctrack/run_tracker_maps.py " + str(run_type) + " " + str(min_run_number) + " " + str(max_run_number)
    tracker_maps_command = "python /home/apatil/test_script.py " + str(
        run_type) + " " + str(min_run_number) + " " + str(max_run_number)
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
    context = {}

    if request.method == 'GET':
        return render(request, "trackermaps/trackermaps.html")

    # is_ajax has been deprecated
    # https://stackoverflow.com/questions/63629935/django-3-1-and-is-ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        min_run_number = request.POST.get("min", None)
        max_run_number = request.POST.get("max", None)
        run_type = request.POST.get("type", None)
        runs_list = request.POST.get("list", None)
        if runs_list:
            try:
                runs_list = list(
                    map(
                        int,
                        re.split(
                            " , | ,|, |,| ",
                            re.sub('\s+', ' ', runs_list).lstrip().rstrip())))
            except ValueError:
                context = {
                    "message":
                    "Run list should contains only numbers of runs separated by comma or space"
                }
                return render(request, "certifier/404.html", context)

        if min_run_number and max_run_number and not runs_list:
            run_tracker_maps(run_type, min_run_number, max_run_number)
            print(min_run_number, max_run_number, run_type)
        else:
            print(runs_list, run_type)

    return render(request, "trackermaps/trackermaps.html")
