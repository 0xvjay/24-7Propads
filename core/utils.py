import calendar

from django.utils import timezone


def get_date_range():
    """Calculate start and end dates for user join metrics."""
    now = timezone.now()
    current_year, current_month = now.year, now.month
    start_year = current_year - 1
    start_month = current_month + 1
    if start_month > 12:
        start_month = 1
        start_year += 1
    start_date = timezone.datetime(start_year, start_month, 1).date()

    last_day = calendar.monthrange(current_year, current_month)[1]
    end_date = timezone.datetime(current_year, current_month, last_day).date()
    return start_date, end_date
