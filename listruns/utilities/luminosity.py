from decimal import Decimal
from listruns.utilities.manip import strip_trailing_zeros

CONVERSION_MAP = {
    r"pb^{-1}": {"ascii": "/pb", "default": "pb⁻¹", "factor": 1},
    r"{\mu}b^{-1}": {"ascii": "/ub", "default": "µb⁻¹", "factor": 1e-6},
}


def convert_luminosity_to_pb(
    int_luminosity: float = None, luminosity_units: str = "pb^{-1}"
) -> float:
    return float(int_luminosity * CONVERSION_MAP[luminosity_units]["factor"])


def format_integrated_luminosity(
    int_luminosity: float = None, luminosity_units: str = "pb^{-1}", to_ascii=False
) -> float:
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

    if int_luminosity is None:
        int_luminosity = 0

    formatted_luminosity = ""

    value = convert_luminosity_to_pb(int_luminosity, luminosity_units)

    # Convert /pb to /ub if very small /pb value
    if f"{value:.3f}" == "0.000":
        value = 1e6 * value
        value_string = f"{value:.3f}"
        formatted_value = strip_trailing_zeros(value_string)
        formatted_units = CONVERSION_MAP[r"{\mu}b^{-1}"][
            "ascii" if to_ascii else "default"
        ]
    else:
        value_string = f"{value:.3f}"
        formatted_value = strip_trailing_zeros(value_string)
        formatted_units = CONVERSION_MAP["pb^{-1}"]["ascii" if to_ascii else "default"]

    formatted_luminosity = f"{formatted_value} {formatted_units}"
    return formatted_luminosity
