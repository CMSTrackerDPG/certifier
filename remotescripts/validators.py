from django.core.exceptions import ValidationError
from remotescripts.utilities import split_with_spaces_commas
from django.utils.regex_helper import _lazy_re_compile
from django.core.validators import RegexValidator


def validate_bash_script(value):
    BANNED_STR = ["&", "&&", ";"]
    if any((s in value for s in BANNED_STR)):
        raise ValidationError(
            f"Invalid characters detected. Banned strings are: {BANNED_STR}'"
        )


string_validator = RegexValidator(
    _lazy_re_compile(r"^[a-zA-Z0-9_,]*$"),
    message=("Value must be an alphanumeric string."),
    code="invalid",
)

# Same as string, no comma
choice_validator = RegexValidator(
    _lazy_re_compile(r"^[a-zA-Z0-9_]*$"),
    message=("Value must be an alphanumeric string."),
    code="invalid",
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
    return values
