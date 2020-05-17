from django import template

register = template.Library()


@register.filter
def humanize_size(value):
    """Converts a bytes into human readable format. Modification of jmoiron/humanize lib"""

    base = 1024
    value_bytes = float(value)
    abs_bytes = abs(value_bytes)

    if abs_bytes < base:
        return "%dB" % value_bytes

    for index, suffix in enumerate('KMGTPEZY'):
        unit = base ** (index + 2)
        if abs_bytes < unit:
            return f'{int(base * value_bytes / unit)}{suffix}B'
    # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
    # pylint: disable=undefined-loop-variable
    return f'{int(base * value_bytes / unit)}{suffix}B'
