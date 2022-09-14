import calendar
import json


def create_callback_data(option, year, month, day):
    return f"{option};{year};{month};{day}"


def create_calendar(year, month):
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
