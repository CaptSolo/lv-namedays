"""
A program for working with the Latvian name day calendar.

It can display today's name days and look up the name day date
for a specific name.
"""

import json
from importlib.resources import files


NAMEDAY_LIST = "tradic_vardadienu_saraksts.json"


def read_namedays():
    """Read the name day data from the JSON file."""

    data_path = files('lv_namedays.data').joinpath(NAMEDAY_LIST)
    
    with data_path.open('r', encoding='utf-8') as f:
        namedays = json.load(f)

    return namedays

def get_date_for_name(name):

    namedays = read_namedays()

    # Make search case insensitive
    namedays = {date: [n.lower() for n in names] for date, names in namedays.items()}

    # Search for the name in the calendar
    for date, names in namedays.items():
        if name.lower() in names:
            return date
    return None
