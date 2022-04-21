from decimal import Decimal

from listruns.utilities.manip import strip_trailing_zeros


def format_integrated_luminosity(int_luminosity, to_ascii=False):
    """
    Example:
    >>> format_integrated_luminosity(Decimal("0.000000266922"))
    '0.267 µb⁻¹'
    >>> format_integrated_luminosity(Decimal("1.12345678901234567890"))
    '1.123 pb⁻¹'

    :param int_luminosity: integrated luminosity value in 1/pb^-1
    :return: Formatted luminosity with 3 decimal points precision
    """
    if int_luminosity == None:
        int_luminosity = 0
    value = Decimal(int_luminosity)
    if '{:.3f}'.format(value) == "0.000":
        value = Decimal("1E6") * value
        value_string = "{:.3f}".format(value)
        formatted_value = strip_trailing_zeros(value_string)
        if to_ascii:
            return "{} /ub".format(formatted_value)
        return "{} µb⁻¹".format(formatted_value)

    value_string = "{:.3f}".format(value)
    formatted_value = strip_trailing_zeros(value_string)
    if to_ascii:
        return "{} /pb".format(formatted_value)
    return "{} pb⁻¹".format(formatted_value)
