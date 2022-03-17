import re
import time
import logging
import threading
import paramiko
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

TEST_BASH_SCRIPT = """
echo Received commands: $1 $2

for i in {1..10}
do
	echo "heheheeh kalispera filoi mou" $i
	sleep 1
done

"""


def send_channel_message(channel_layer: RedisChannelLayer, group_name: str,
                         message: str) -> None:
    """
    Function that sends a message
    """

    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'channel_message',
        'message': message
    })


def run_tracker_maps(run_type: str, run_number_list: list) -> Bool:
    """
    Function that connects to vocms066 using the env-supplied username/password
    and executes the script to generate specific tracker maps.
    """
    tracker_maps_command = f"cd /data/users/event_display/ShiftRun3/TkMapGeneration/CMS* &&"\
    " bash /data/users/event_display/ShiftRun3/TkMapGeneration/tkmapsFromCertHelper.sh"\
    f" {str(run_type)} {str(run_number_list)}"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect("vocms066",
                username=settings.DJANGO_SECRET_ACC,
                password=settings.DJANGO_SECRET_PASS)
    logger.debug(f"Executing '{tracker_maps_command}'")
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(TEST_BASH_SCRIPT,
    #                                                      get_pty=True)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(tracker_maps_command,
                                                         get_pty=True)
    channel_layer = get_channel_layer()

    # Function that reads output byte by byte,
    # yielding whole lines
    def line_buffered(f):
        line_buf = b""
        while not f.channel.exit_status_ready():
            line_buf += f.read(1)
            time.sleep(0.01)
            if line_buf.endswith(b'\n'):
                yield line_buf
                line_buf = b""

    # Spit out output to channel layer
    for line in line_buffered(ssh_stdout):
        line = line.decode('utf-8', errors='ignore')
        print(line)
        send_channel_message(channel_layer, "output_group", f"{line}")

    send_channel_message(channel_layer, "output_group", "GENERATION ENDED\n")

    # Verify script's exit status
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

    # is_ajax has been deprecated
    # https://stackoverflow.com/questions/63629935/django-3-1-and-is-ajax
    if request.method == 'POST' and request.META.get(
            'HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
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

        # Start on a separate thread
        threading.Thread(target=run_tracker_maps,
                         args=(run_type, runs_list)).start()

    return render(request, "trackermaps/trackermaps.html")
