import calendar
import json


def create_callback_data(option: str, year: int, month: int, day: int) -> str:
    """
    Creating the callback data for each button
    :param option: the action to do with each button
    :param year: transmitted year
    :param month: transmitted month
    :param day: transmitted day
    :return: callback data for each button
    """
    return f"{option};{year};{month};{day}"


def create_calendar(year: int, month: int) -> json:
    """
    Creating the calendar for each month using inline keyboard.
    Creating the option to change the month and the year
    :param year: transmitted year
    :param month: transmitted month
    :return: json-file containing the calendar for each month
    """
    calendar_json = {"inline_keyboard": []}
    row = [{"text": f"{calendar.month_name[month]}, {year}",
            "callback_data": create_callback_data("IGNORE", year, month, 0)}]
    calendar_json["inline_keyboard"].append(row)

    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append({"text": day, "callback_data": create_callback_data("IGNORE", year, month, 0)})
    calendar_json["inline_keyboard"].append(row)

    help_calendar = calendar.monthcalendar(year, month)
    for week in help_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append({"text": " ", "callback_data": create_callback_data("IGNORE", year, month, 0)})
            else:
                row.append({"text": f"{day}", "callback_data": create_callback_data("DAY", year, month, day)})
        calendar_json["inline_keyboard"].append(row)

    row = [
        {"text": "<", "callback_data": create_callback_data("PREV_MONTH", year, month, 0)},
        {"text": " ", "callback_data": create_callback_data("IGNORE", year, month, 0)},
        {"text": ">", "callback_data": create_callback_data("NEXT_MONTH", year, month, 0)}
    ]
    calendar_json["inline_keyboard"].append(row)

    return json.dumps(calendar_json)
