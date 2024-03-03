from datetime import datetime
from dateutil.relativedelta import relativedelta

## 
def clean_select_objects_split_str(input_str):
    """Rename and Clean certain chart objects like North, South Node and Fortuna"""
    cleaned_str = (input_str.strip('<').strip('>')
                          .replace("North Node", "Rahu")
                          .replace("South Node", "Ketu")
                          .replace("Pars Fortuna", "Fortuna"))
    return cleaned_str.split()

def pretty_data_table(named_tuple_data : list):
    """Converts a list of NamedTuple Collections to a PrettyTable"""
    from prettytable import PrettyTable
    # Create a PrettyTable instance
    table = PrettyTable()

    # Add field names (column headers)
    table.field_names = named_tuple_data[0]._fields 

    # Add rows
    for data in named_tuple_data:
        table.add_row(data)

    return table

def dms_to_decdeg(dms_str: str):
    """
    This function converts a string input in Degrees:Mins:Secs to Decimal Degrees
    """
    dms = dms_str.split(':')
    degrees = float(dms[0])
    minutes = float(dms[1])
    seconds = float(dms[2])
    return round(degrees + (minutes/60) + (seconds/3600), 4)


def dms_to_mins(dms_str: str):
    """
    This function converts a string input in Degrees:Mins:Secs to total minutes.
    """
    dms = dms_str.split(':')
    degrees = int(dms[0])
    minutes = int(dms[1])
    seconds = int(dms[2])
    total_minutes = degrees * 60 + minutes + seconds / 60
    return round(total_minutes, 2)  

def dms_difference(dms1_str: str, dms2_str: str):
    """
    This function computes the difference between two degree:mins:secs string objects
    and returns the difference as a degree:mins:secs string.
    """
    def dms_to_seconds(dms_str):
        dms = dms_str.split(':')
        degrees = int(dms[0])
        minutes = int(dms[1])
        seconds = int(dms[2])
        total_seconds = degrees * 3600 + minutes * 60 + seconds
        return total_seconds

    def seconds_to_dms(seconds):
        degrees = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{int(degrees)}:{int(minutes)}:{int(seconds)}"

    dms1_seconds = dms_to_seconds(dms1_str)
    dms2_seconds = dms_to_seconds(dms2_str)

    diff_seconds = abs(dms1_seconds - dms2_seconds)

    return seconds_to_dms(diff_seconds)


def convert_years_ymdhm(years):
    """
    This function converts decimal years into years, months, days, hours, and minutes.
    """
    # Constants
    months_per_year = 12
    days_per_month = 30  # Approximation
    hours_per_day = 24
    minutes_per_hour = 60

    # Compute the breakdown
    whole_years = int(years)
    months = (years - whole_years) * months_per_year
    whole_months = int(months)
    days = (months - whole_months) * days_per_month
    whole_days = int(days)
    hours = (days - whole_days) * hours_per_day
    whole_hours = int(hours)
    minutes = (hours - whole_hours) * minutes_per_hour
    whole_minutes = int(minutes)

    return whole_years, whole_months, whole_days, whole_hours, whole_minutes

def compute_new_date(start_date : tuple, diff_value : float, direction: str):
    """
    This function computes a new date and time given an initial date and time and a time difference.
    """
    # Unpack start_date and diff_params
    year, month, day, hour, minute = start_date
    years, months, days, hours, minutes = convert_years_ymdhm(diff_value)

    # Create initial datetime object
    initial_date = datetime(year, month, day, hour, minute)

    # Compute relativedelta object
    time_difference = relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes)

    # Compute new date
    if direction == 'backward':
        new_date = initial_date - time_difference
    elif direction == 'forward':
        new_date = initial_date + time_difference
    else:
        raise ValueError("direction must be either 'backward' or 'forward'")

    return new_date