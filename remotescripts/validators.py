from django.core.exceptions import ValidationError
from remotescripts.utilities import split_with_spaces_commas


def validate_bash_script(value):
    BANNED_STR = ["&"]
    if any((s in value for s in BANNED_STR)):
        raise ValidationError(
            f"Invalid characters detected. Banned strings are: {BANNED_STR}'"
        )


def validate_comma_space_separated_values_string(value):
    if not value:
        raise ValidationError("At least one value should be entered")
    try:
        values = split_with_spaces_commas(value)
        if len(values) < 1:
            raise ValidationError("At least one value should be entered")

    except ValueError:
        raise ValidationError(
            "Value should contain only strings separated by comma or space"
        )
