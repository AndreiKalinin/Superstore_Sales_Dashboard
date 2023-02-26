def num_format(x):
    """Set numeric format"""
    return '{:,}'.format(round(x)).replace(',', ' ')


def percent_format(x):
    """Set percent format"""
    return f'change: {round(x * 100, 1)}%'


def value_color(x):
    """Set conditional color"""
    if x > 0:
        return {'color': 'green'}
    return {'color': 'red'}
