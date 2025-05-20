"""
A program for working with the Latvian name day calendar.

It can display today's name days and look up the name day date
for a specific name.
"""

import json
from importlib.resources import files


NAMEDAY_LIST = "tradic_vardadienu_saraksts.json"
NAMEDAY_LIST_EXTENDED = "paplasinatais_saraksts.json"

def read_namedays() -> dict:
    """Read the name day data from the main namedays JSON file."""

    data_path = files('lv_namedays.data').joinpath(NAMEDAY_LIST)
    
    with data_path.open('r', encoding='utf-8') as f:
        namedays = json.load(f)

    return namedays

def read_namedays_ext() -> dict:
    """Read the name day data from the extended namedays JSON file."""

    data_path = files('lv_namedays.data').joinpath(NAMEDAY_LIST_EXTENDED)
    
    with data_path.open('r', encoding='utf-8') as f:
        namedays_ext = json.load(f)

    return namedays_ext


class NameDayDB:
    def __init__(self):
        self.namedays = read_namedays()
        self.namedays_ext = read_namedays_ext()

    def get_names_for_date(self, date:str, extended:bool = False) -> list | None:
        """
        Returns a list of names for a given nameday date.
        The date should be in the format "MM-DD".
        """
        
        if not extended:
            return self.namedays.get(date, None)
        else:
            return self.namedays_ext.get(date, None)

    def get_date_for_name(self, name:str, extended:bool = False) -> str | None:
        """
        Returns the nameday date for a given name.
        """

        if not extended:
            namedays = self.namedays
        else:
            namedays = self.namedays_ext

        namedays = {date: [n.lower() for n in names] for date, names in namedays.items()}

        # Search for the name in the calendar
        for date, names in namedays.items():
            if name.lower() in names:
                return date

        # Name was not found
        return None

