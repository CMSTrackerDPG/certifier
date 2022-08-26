from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)


def validate_list_length(value):
    if not isinstance(value, list):
        raise ValidationError(
            _("%(value)s is not a list"),
            params={"value": value},
        )
    elif len(value) < 1:
        raise ValidationError(
            _("%(value)s is an empty list"),
            params={"value": value},
        )
