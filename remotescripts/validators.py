from django.core.exceptions import ValidationError


def validate_bash_script(value):
    if "&" in value:
        raise ValidationError(f"Invalid characters in '{value}'")
