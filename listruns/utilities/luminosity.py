from decimal import Decimal
from listruns.utilities.manip import strip_trailing_zeros


def format_integrated_luminosity(
    int_luminosity: float = None, luminosity_units: str = "pb^{-1}", to_ascii=False
):
    """
    Example:
    >>> format_integrated_luminosity(Decimal("0.000000266922"))
    '0.267 µb⁻¹'
    >>> format_integrated_luminosity(Decimal("1.12345678901234567890"))
    '1.123 pb⁻¹'

    :param int_luminosity: integrated luminosity value
    :param luminosity_units: units luminosity is counted in
    :return: Formatted luminosity with 3 decimal points precision
    """
    CONVERSION_MAP = {
        r"pb^{-1}": {"ascii": "/pb", "default": "pb⁻¹", "exponent": 12},
        r"{\mu}b^{-1}": {"ascii": "/ub", "default": "µb⁻¹", "exponent": 6},
    }
    if int_luminosity is None:
        int_luminosity = 0

    formatted_luminosity = ""
    value = Decimal(int_luminosity)

    # Convert /pb to /ub if very small /pb value
    if f"{value:.3f}" == "0.000" and CONVERSION_MAP[luminosity_units]["exponent"] == 12:
        value = Decimal("1E6") * value
        value_string = f"{value:.3f}"
        formatted_value = strip_trailing_zeros(value_string)
        formatted_units = CONVERSION_MAP[r"{\mu}b^{-1}"][
            "ascii" if to_ascii else "default"
        ]
    else:
        value_string = f"{value:.3f}"
        formatted_value = strip_trailing_zeros(value_string)
        formatted_units = CONVERSION_MAP[luminosity_units][
            "ascii" if to_ascii else "default"
        ]

    formatted_luminosity = f"{formatted_value} {formatted_units}"
    return formatted_luminosity
