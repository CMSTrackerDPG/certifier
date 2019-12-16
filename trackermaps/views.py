from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import subprocess
import re
import os
import paramiko

def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        {
            'type': 'channel_message',
            'message': message
        }
    )

def run_tracker_maps(run_type, min_run_number, max_run_number):
    tracker_maps_command = "python /home/cctrack/run_tracker_maps.py " + str(run_type) + " " + str(min_run_number) + " " + str(max_run_number)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("vocms066", username="", password="")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(tracker_maps_command, get_pty=True)

    for line in iter(ssh_stdout.readline, ""):
        send_channel_message("output_group",">_: " + line)
    send_channel_message("output_group", "PROCESS HAS ENDED")

    if ssh_stderr:
        return False
    return True

def maps(request):
    context = {}

    if request.method == 'GET':
        return render(request, "trackermaps/trackermaps.html")

    if request.is_ajax():
        min_run_number = request.POST.get("min", None)
        max_run_number = request.POST.get("max", None)
        run_type = request.POST.get("type", None)
        print(min_run_number + " " + max_run_number + " " + run_type)
        runs_list = request.POST.get("list", None)
        if runs_list:
            try:
                runs_list = list(map(int, re.split(" , | ,|, |,| ", re.sub('\s+', ' ', runs_list).lstrip().rstrip())))
            except ValueError:
                context = {"message": "Run list should contains only numbers of runs separated by comma or space"}
                return render(request, "certifier/404.html", context)


        if min_run_number and max_run_number and not runs_list:
            run_tracker_maps(run_type, min_run_number, max_run_number)
            print(min_run_number, max_run_number, run_type)
        else:
            print(runs_list, run_type)

    return render(request, "trackermaps/trackermaps.html")
