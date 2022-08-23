from django.core.management.base import BaseCommand, CommandError
from remotescripts.models import ScriptConfigurationBase


class Command(BaseCommand):
    help = (
        "Clears the running status of all remotescripts. To be used on server restart"
    )

    def handle(self, *args, **options):
        scripts = ScriptConfigurationBase.objects.all()
        count = 0
        for script in scripts:
            if script.is_running:
                script.is_running = False
                script.save()
                count += 1
        if count:
            self.stdout.write(
                self.style.SUCCESS("Cleared 'running' status of %s scripts" % count)
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("No scripts with status 'running' were found")
            )
