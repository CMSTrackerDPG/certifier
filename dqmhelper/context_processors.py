"""
Custom context processors
"""
from django.conf import settings


def global_context(request):
    """
    Add here context which should available to all templates
    """
    return {'certhelper_version': settings.CERTHELPER_VERSION}
