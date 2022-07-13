import re
from django.core.exceptions import ValidationError


def validate_bash_script(value):
    BANNED_STR = ["&"]
    if any((s in value for s in BANNED_STR)):
        raise ValidationError(
            f"Invalid characters detected. Banned strings are: {BANNED_STR}'"
        )


def validate_comma_space_separated_values_string(value):
    try:
        values = list(
            map(
                str,
                re.split(
                    " , | ,|, |,| ",
                    re.sub(r"\s+", " ", value).lstrip().rstrip(),
                ),
            )
        )
        if len(values) < 1:
            raise ValidationError("At least one value should be entered")

    except ValueError:
        raise ValidationError(
            "Value should contain only strings separated by comma or space"
        )
