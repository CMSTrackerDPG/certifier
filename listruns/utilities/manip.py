from decimal import Decimal


def strip_trailing_zeros(number_string):
    """
    Example:
    >>> strip_trailing_zeros("1.000")
    '1'
    >>> strip_trailing_zeros("1.12345000")
    '1.12345'
    >>> strip_trailing_zeros("42")
    '42'
    >>> strip_trailing_zeros(Decimal("1.120"))
    '1.12'
    >>> strip_trailing_zeros('0.267')
    '0.267'

    :param number_string:
    :return:
    """
    return str(number_string).rstrip("0").rstrip(".")
