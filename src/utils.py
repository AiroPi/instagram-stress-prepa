import datetime as dt


def progress(start: dt.datetime, current: dt.datetime, end: dt.datetime):
    """
    Returns:
        A float between 0 and 1, representing the progress of the current datetime between the start and end datetimes.
    """
    total = (end - start).total_seconds()
    state = (current - start).total_seconds()
    return state / total


def all_units(delta: dt.timedelta):
    """
    Split a timedelta into units if time.

    Returns:
        A tuple with the following units: (months, days)
    """
    seconds = delta.total_seconds()
    months, rest = divmod(seconds, 3600 * 24 * 30.5)
    # weeks, rest = divmod(rest, 3600 * 24 * 7)
    days, rest = divmod(rest, 3600 * 24)
    # hours, rest = divmod(rest, 3600)
    # minutes, rest = divmod(rest, 60)
    # seconds = rest

    # return tuple(int(v) for v in (months, weeks, days, hours, minutes, seconds))
    return tuple(int(v) for v in (months, days))
