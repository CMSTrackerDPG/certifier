from django.core.exceptions import ValidationError


def validate_bash_script(value):
    BANNED_STR = ["&"]
    if any((s in value for s in BANNED_STR)):
        raise ValidationError(
            f"Invalid characters detected. Banned strings are: {BANNED_STR}'"
        )
