import re

from django import template

register = template.Library()


@register.filter(is_safe=True)
def intspace(value):
    """Convert an integer to a string containg spaces every three digits.

    E.g. 3000 becomes '3 000' and 45000 becomes '45 000'.
    """
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1> \g<2>', orig)
    if orig == new:
        return new
    return intspace(new)
