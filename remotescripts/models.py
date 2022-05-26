import tempfile
import logging
from abc import abstractclassmethod
import subprocess
import paramiko
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from remotescripts.validators import validate_bash_script
from model_utils.managers import InheritanceManager

logger = logging.getLogger(__name__)


class ScriptConfigurationBase(models.Model):
    """
    Base model for configuration common across different
    type of scripts to execute
    """

    objects = InheritanceManager()
    title = models.CharField(
        max_length=50, help_text="Script title to display", null=True
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
        num_pos_args = self.positional_arguments.count()
        num_kw_args = self.keyword_arguments.count()
        if num_pos_args > 0:
            if len(args) != num_pos_args:
                raise TypeError(
                    f"Script requires {num_pos_args} positional argument(s) but {len(args)} was given"
                )
            p = self.positional_arguments.filter().order_by("position")

            for i, _p in enumerate(p):
                # TODO Typecheck
                cmd += f" {str(args[i])}"

        if num_kw_args > 0:
            if len(kwargs) != num_kw_args:
                raise TypeError(
                    f"Script requires {num_kw_args} keyword argument(s) but {len(kwargs)} was given"
                )
            k = self.keyword_arguments.all()
            for _k in k:
                if _k.keyword not in kwargs:
                    raise TypeError(f"Missing keyword argument '{_k.keyword}'")
                cmd += f" {str(_k)}{kwargs[_k.keyword]}"
        return cmd

    def save(self, *args, **kwargs):
        self.base_command = str(self.base_command).replace("\r", "")
        super().save(*args, **kwargs)

    @abstractclassmethod
    def execute(self, *args, **kwargs):
        pass


class BashScriptConfiguration(ScriptConfigurationBase):
    """
    Model for local bash script configuration
    """

    def execute(self, *args, **kwargs):
        """
        The idea here is to save the script in a temp file,
        then pass it to bash via subprocess.

        Not tested a lot, but the main idea works.
        """
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
        cmd_to_execute = self._form_command(*args, **kwargs)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.host,
            username=getattr(settings, self.env_secret_username),
            password=getattr(settings, self.env_secret_password),
            port=self.port,
        )
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
    name = models.CharField(max_length=20, null=True, default="")
    type = models.CharField(
        max_length=3, choices=ARGUMENT_CHOICES, default=ARGUMENT_STR
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class ScriptPositionalArgument(ScriptArgumentBase):
    position = models.PositiveSmallIntegerField(
        help_text="Position to be placed after command.",
        validators=[MinValueValidator(limit_value=1)],
    )
    mother_script = models.ForeignKey(
        ScriptConfigurationBase,
        on_delete=models.CASCADE,
        help_text="Script instance this argument applies to",
        null=False,
        related_name="positional_arguments",
    )

    class Meta:
        unique_together = [["position", "mother_script"]]

    def __str__(self):
        return (
            f"{self.name} (Pos:{self.position}) for "
            f"{ScriptConfigurationBase.objects.get_subclass(id=self.mother_script.pk)}"
        )


class ScriptKeywordArgument(ScriptArgumentBase):
    SEPARATOR_SPACE = " "
    SEPARATOR_EQUALS = "="
    SEPARATOR_CHOICES = ((SEPARATOR_SPACE, "Space"), (SEPARATOR_EQUALS, "="))
    keyword = models.CharField(
        max_length=50,
        help_text="Keyword name for this argument",
        null=False,
        default="keyword",
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
