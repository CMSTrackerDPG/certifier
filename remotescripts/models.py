import tempfile
import logging
from abc import abstractclassmethod
import subprocess
import paramiko
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from remotescripts.validators import validate_bash_script
from model_utils.managers import InheritanceManager

logger = logging.getLogger(__name__)


class ScriptConfigurationBase(models.Model):
    objects = InheritanceManager()
    title = models.CharField(
        max_length=20, help_text="Script title to display", null=True
    )

    base_command = models.TextField(
        max_length=500,
        help_text="Base command to run",
        null=False,
        validators=[validate_bash_script],
    )
    show_stdout = models.BooleanField(help_text="Show stdout", default=True)
    show_stderr = models.BooleanField(help_text="Show stderr", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _form_command(self, *args, **kwargs) -> str:
        cmd = str(self.base_command)
        print(type(cmd), cmd)
        if self.positional_arguments.count() > 0:
            pass

        if self.keyword_arguments.count() > 0:
            k = self.keyword_arguments
            print(k)
        return cmd

    def save(self, *args, **kwargs):
        self.base_command = str(self.base_command).replace("\r", "")
        super().save(*args, **kwargs)

    @abstractclassmethod
    def execute(self, *args, **kwargs):
        pass


class BashScriptConfiguration(ScriptConfigurationBase):
    def execute(self, *args, **kwargs):
        cmd_to_execute = self._form_command(*args, **kwargs)
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(cmd_to_execute.encode())
            with subprocess.Popen(["bash", fp.name], stdout=subprocess.PIPE) as process:
                output, error = process.communicate()
            print(output)

    def __str__(self) -> str:
        return f"{self.title} (Local)"


class RemoteScriptConfiguration(ScriptConfigurationBase):
    """
    Model storing configuration for executing scripts on remote hosts
    """

    CONNECTION_SSH_KB = "ssh_kb"
    CONNECTION_PROTOCOL_CHOICES = [(CONNECTION_SSH_KB, "SSH - keyboard interactive")]

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
        default=22,
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

    @staticmethod
    def _line_buffered(f):
        while not f.channel.exit_status_ready():
            for line in f:
                yield line

    def execute(self, *args, **kwargs) -> bool:
        """
        Method that executes remote script
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.host,
            username=getattr(settings, self.env_secret_username),
            password=getattr(settings, self.env_secret_password),
            port=self.port,
        )
        cmd_to_execute = self._form_command(*args, **kwargs)
        logger.debug(f"Executing '{cmd_to_execute}'")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            cmd_to_execute, get_pty=True
        )

        for line in self._line_buffered(ssh_stdout):
            # line = line.decode("utf-8", errors="ignore")  # Convert bytes to str
            logger.debug(line)

        exit_status = ssh_stdout.channel.recv_exit_status()
        if exit_status:
            logger.warning(f"Remote process exited with status {exit_status}")
            return False
        logger.info("Remote process terminated with no errors")
        return True

    def __str__(self) -> str:
        return f"{self.title} ({self.get_connection_protocol_display()})"


class ScriptOutputFile(models.Model):
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


class ScriptArgumentBase(models.Model):
    ARGUMENT_INT = "INT"
    ARGUMENT_STR = "STR"
    ARGUMENT_CHOICES = ((ARGUMENT_INT, "Integer"), (ARGUMENT_STR, "String"))
    argument_type = models.CharField(choices=ARGUMENT_CHOICES, max_length=3)


class ScriptPositionalArgument(ScriptArgumentBase):
    position = models.PositiveIntegerField(
        help_text="Position to be placed after command. 0 means don't care"
    )
    mother_script = models.ForeignKey(
        ScriptConfigurationBase,
        on_delete=models.CASCADE,
        help_text="Script instance this argument applies to",
        null=False,
        related_name="positional_arguments",
    )

    def __str__(self):
        return f"Positional argument (Pos:{self.position}) for {ScriptConfigurationBase.objects.get_subclass(id=self.mother_script.pk)}"


class ScriptKeywordArgument(ScriptArgumentBase):
    SEPARATOR_SPACE = " "
    SEPARATOR_EQUALS = "="
    SEPARATOR_CHOICES = ((SEPARATOR_SPACE, "Space"), (SEPARATOR_EQUALS, "="))
    keyword = models.CharField(
        max_length=50, help_text="Keyword name for this argument", null=False
    )
    separator = models.CharField(
        max_length=2,
        help_text="Separator between they keyword name and the argument",
        choices=SEPARATOR_CHOICES,
        default=SEPARATOR_SPACE,
    )
    mother_script = models.ForeignKey(
        ScriptConfigurationBase,
        on_delete=models.CASCADE,
        help_text="Script instance this argument applies to",
        null=False,
        related_name="keyword_arguments",
    )

    def __str__(self):
        return f"--{self.keyword}{self.separator}"
