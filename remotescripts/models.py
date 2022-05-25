from django.db import models
from django.core.validators import MaxValueValidator


class RemoteScriptConfiguration(models.Model):
    """
    Model storing configuration for executing scripts on remote hosts
    """

    CONNECTION_SSH_KB = "ssh_kb"
    CONNECTION_PROTOCOL_CHOICES = [(CONNECTION_SSH_KB, "SSH - keyboard interactive")]

    title = models.CharField(
        max_length=20, help_text="Script title to display", null=True
    )

    command = models.CharField(
        max_length=500, help_text="Remote command to run", null=False
    )
    host = models.CharField(
        max_length=50,
        help_text="Remote host to run the command on",
        null=False,
        blank=False,
    )
    port = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=65535)],
        help_text="Remote host port to connect to",
        null=True,
        default=23,
    )
    connection_protocol = models.CharField(
        max_length=10,
        choices=CONNECTION_PROTOCOL_CHOICES,
        help_text="Connection protocol to use",
        default=CONNECTION_SSH_KB,
    )
    env_secret_username = models.CharField(
        max_length=20,
        help_text="Environment variable name where username is stored",
        null=True,
    )
    env_secret_password = models.CharField(
        max_length=20,
        help_text="Environment variable name where password is stored",
        null=True,
    )

    show_stdout = models.BooleanField(help_text="Show stdout", default=True)
    show_stderr = models.BooleanField(help_text="Show stderr", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RemoteScriptOutputFile(models.Model):
    """
    Model representing a file output of a remote script
    """

    mother_script = models.ForeignKey(
        RemoteScriptConfiguration,
        on_delete=models.CASCADE,
        help_text="Script instance this file is generated from",
        null=False,
        related_name="output_files",
    )
    directory = models.CharField(
        max_length=255,
        help_text="Directory where the output file is to be found",
        default="~",
    )
    filename_regex = models.CharField(
        max_length=100,
        help_text="Regex to use in directory to find the file",
        default=r"(?P<filename>.+)?\.txt",
    )
