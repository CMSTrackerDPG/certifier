import re
import logging
import threading
import paramiko
from django.conf import settings
from django.views.generic import DetailView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
from remotescripts.models import RemoteScriptConfiguration, RemoteScriptOutputFile

logger = logging.getLogger(__name__)

# TEST_BASH_SCRIPT = """
# python3 -c "import salkdfklsadf"
# """
TEST_BASH_SCRIPT = """
echo Received commands: $1 $2

for i in {1..10}
do
echo "heheheeh kalispera filoi mou" $i
sleep 1
done
"""


class RemoteScriptExecutionView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template = ""
    context = {}
    remote_command = None
    configuration = None
    model = RemoteScriptConfiguration

    def test_func(self):
        """
        Function used by the UserPassesTestMixin to
        test rights before allowing acess to the View
        """
        return (
            hasattr(self.request.user, "has_shifter_rights")
            and self.request.user.has_shifter_rights
        )

    def get(self, request):
        return render(request, self.template, self.context)

    def execute_command(self):
        if not self.remote_command:
            raise Exception("No command specified!")
        channel_layer = get_channel_layer()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.send_channel_message(
            channel_layer,
            "output_group",
            f"-------- CONNECTING TO {self.object.host} --------\n",
        )

    @staticmethod
    def send_channel_message(
        channel_layer: RedisChannelLayer, group_name: str, message: str
    ) -> None:
        """
        Function that sends a message
        """
        async_to_sync(channel_layer.group_send)(
            group_name, {"type": "channel_message", "message": message}
        )


class TrackerMapsView(RemoteScriptExecutionView):
    template = "remotescripts/trackermaps.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def post(self, request):
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            run_type = request.POST.get("type", None)
            runs_list = request.POST.get("list", None)
            logger.info(
                f"Got trackermaps generation request for {run_type}: {runs_list}"
            )
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
                    logger.debug(f"Parsed runs list: {runs_list}")
                except ValueError:
                    context = {
                        "message": "Run list should contain only numbers of runs separated by comma or space"
                    }
                    return JsonResponse(context, status=400)
                except Exception as e:
                    context = {"message": repr(e)}
                    return JsonResponse(context, status=500)

            # Start on a separate thread
            threading.Thread(
                target=self.run_tracker_maps, args=(run_type, runs_list)
            ).start()

    def get(self, request):
        return super().get(request)

    def run_tracker_maps(self, run_type: str, run_number_list: list) -> bool:
        """
        Function that connects to vocms066 using the env-supplied username/password
        and executes the script to generate specific tracker maps.
        """
        # tracker_maps_command = (
        #     "cd /data/users/event_display/ShiftRun3/TkMapGeneration/CMS* &&"
        #     " bash /data/users/event_display/ShiftRun3/TkMapGeneration/tkmapsFromCertHelper.sh"
        #     f" {str(run_type)} {''.join(str(run_number)+' ' for run_number in run_number_list)}"
        # )
        tracker_maps_command = TEST_BASH_SCRIPT

        channel_layer = get_channel_layer()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.send_channel_message(
            channel_layer, "output_group", "-------- CONNECTING TO vocms066 --------\n"
        )
        try:
            ssh.connect(
                "vocms066",
                username=settings.DJANGO_SECRET_ACC,
                password=settings.DJANGO_SECRET_PASS,
            )
        except Exception as e:
            logger.exception(e)
            self.send_channel_message(channel_layer, "output_group", repr(e))
            raise
        self.send_channel_message(
            channel_layer, "output_group", "-------- CONNECTED --------\n"
        )
        self.send_channel_message(
            channel_layer, "output_group", "-------- SCRIPT STARTED --------\n"
        )
        logger.debug(f"Executing '{tracker_maps_command}'")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            tracker_maps_command, get_pty=True
        )

        # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(TEST_BASH_SCRIPT,
        #                                                      get_pty=True)

        # Function that reads output byte by byte,
        # yielding whole lines
        def line_buffered(f):
            # line_buf = b""
            while not f.channel.exit_status_ready():
                for line in f:
                    yield line

        # Spit out output to channel layer
        for line in line_buffered(ssh_stdout):
            # line = line.decode('utf-8', errors='ignore')  # Convert bytes to str
            logger.debug(line)
            self.send_channel_message(channel_layer, "output_group", f"{line}")

        self.send_channel_message(
            channel_layer, "output_group", "-------- SCRIPT STOPPED --------\n"
        )

        for line in line_buffered(ssh_stdin):
            line = line.decode("utf-8", errors="ignore")  # Convert bytes to str
            self.send_channel_message(channel_layer, "output_group", f"{line}")

        # Verify script's exit status
        exit_status = ssh_stdout.channel.recv_exit_status()
        if exit_status:
            logger.warning(f"Remote process exited with status {exit_status}")
            return False
        logger.info("Remote process terminated with no errors")
        return True
