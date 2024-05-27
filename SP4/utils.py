import datetime
from datetime import timedelta
import requests
import base64
import json

from data import *


def api_call(frame):
    """
    Call the given API with the given frame information and return the number received
    :param frame: Contextual frame
    :return: Number of accidents, from_time, to_time
    """
    # Given url for the API
    url = "https://d2g9cow0nr2qp.cloudfront.net/"

    # Get the time range in seconds since epoch
    from_time, to_time = frame_time_to_secs_since_epoch(frame.get_time())

    # Prepare the data for the API
    data = {
        "from": from_time,
        "to": to_time,
        "all": "true"
    }

    # Encode the data to base64
    json_data = json.dumps(data)
    base64_data = base64.b64encode(json_data.encode()).decode()

    # Prepare the parameters for the API
    params = {
        'q': base64_data
    }

    # Call the API
    response = requests.get(url, params=params)
    response = response.json()

    # Filter the response based on the frame
    place = frame.get_place()
    accident = frame.get_accident()

    # I don't trust the API at all
    try:
        return int(response[place][accident]), datetime.datetime.fromtimestamp(from_time), datetime.datetime.fromtimestamp(to_time)
    except:
        return 0, datetime.datetime.fromtimestamp(from_time), datetime.datetime.fromtimestamp(to_time)


def get_time_range(time):
    """
    Get the time range from the given time
    :param time: Time
    :return: Time range (day, week, month, year) as string
    """
    time_range = ""

    if time in day_keys:
        time_range = "day"
    elif time in week_keys:
        time_range = "week"
    elif time in month_keys:
        time_range = "MONth"
    elif time in year_keys:
        time_range = "year"

    return time_range


def get_time_base(time, time_range):
    """
    Get the base time for the given time
    :param time: Time
    :param time_range: Time range
    :return: Base time as datetime
    """
    # Base is today
    base = datetime.datetime.now()

    if time == "yesterday":
        base -= timedelta(days=1)
    elif time == "daybeforeyesterday":
        base -= timedelta(days=2)
    elif time == "week" or time == "mon":
        base -= timedelta(days=base.weekday())
    elif time == "MONth":
        base = base.replace(day=1)
    elif time == "year" or time == "thisyear" or time == "jan":
        base = base.replace(month=1, day=1)
    elif time == "lastyear":
        base = base.replace(year=base.year - 1, month=1, day=1)
    elif time == "tue" or time == "wed" or time == "thu" or time == "fri" or time == "sat" or time == "sun":
        temp = {
            "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6
        }
        base -= timedelta(days=base.weekday() - temp[time])
    elif time == "feb" or time == "mar" or time == "apr" or time == "may" or time == "jun" or time == "jul" \
                       or time == "aug" or time == "sep" or time == "oct" or time == "nov" or time == "dec":
        temp = {
            "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
            "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }
        base = base.replace(month=temp[time], day=1)

    # If the base is in the future, go back
    if time_range == "week":
        if base > datetime.datetime.now():
            base = base.replace(day=base.day - 7)
    elif time_range == "MONth":
        if base > datetime.datetime.now():
            base = base.replace(year=base.year - 1)

    return base


def get_time_offset(decorator):
    """
    Get the offset for the given decorator
    :param decorator: Decorator
    :return: Offset as int (0, -1, -2)
    """
    # Basic offset is "this" -> 0
    offset = 0
    if decorator is not None:
        if decorator == "last":
            offset = -1
        elif decorator == "lastlast":
            offset = -2

    return offset


def apply_time_offset(time, from_time, to_time, time_range, offset):
    """
    Apply the offset to the given time
    :param time: Time
    :param from_time: From time
    :param to_time: To time
    :param time_range: Time range
    :param offset: Offset
    :return: From time, To time
    """
    if time_range == "day":
        from_time += timedelta(days=offset)
        to_time += timedelta(days=offset)
    elif time_range == "week":
        from_time += timedelta(days=7 * offset)
        if time == "mon" or time == "tue" or time == "wed" or time == "thu" or time == "fri" or time == "sat" or time == "sun":
            to_time += timedelta(days=7 * offset)
        else:
            to_time += timedelta(days=7 * offset + 6)
    elif time_range == "MONth":
        from_time = from_time.replace(year=from_time.year + offset)
        to_time = to_time.replace(year=to_time.year + offset)
        # Go to the last day of that month (but minus one since its to 23:59:59)
        temp = {"jan": 31, "feb": 28, "mar": 31, "apr": 30, "may": 31, "jun": 30,
                "jul": 31, "aug": 31, "sep": 30, "oct": 31, "nov": 30, "dec": 31}
        to_time += timedelta(days=temp[time] - 1)
    elif time_range == "year":
        from_time = from_time.replace(year=from_time.year + offset)
        to_time = to_time.replace(year=to_time.year + offset + 1)
        # Go back to the last day of the previous year
        to_time -= timedelta(days=1)

    return from_time, to_time


def frame_time_to_secs_since_epoch(time):
    """
    Convert the time as keys from time_map (+ possibly time_decorators_map) to nanoseconds (from, to)
    """
    decorator = None
    time = time.split(" ")
    if len(time) == 2:
        decorator, time = time
    else:
        time = time[0]

    time_range = get_time_range(time)
    base = get_time_base(time, time_range)
    offset = get_time_offset(decorator)

    from_time = base.replace(hour=0, minute=0, second=0)
    to_time = base.replace(hour=23, minute=59, second=59)

    from_time, to_time = apply_time_offset(time, from_time, to_time, time_range, offset)

    # API doesn't work for 2024 anymore -> subtract a year from everything
    from_time = from_time.replace(year=from_time.year - 1)
    to_time = to_time.replace(year=to_time.year - 1)

    return int(from_time.timestamp()), int(to_time.timestamp())
