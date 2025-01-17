#!/usr/bin/env python3

"""
A program that tells you the Latvian nameday for today.
"""

import datetime as dt
import json
import argparse
import os
import importlib.resources

NAMEDAY_LIST = "tradic_vardadienu_saraksts.json"

def read_namedays():

    current_directory = os.getcwd()
    print("Current Working Directory:", current_directory)

    with importlib.resources.open_text('nameday.data', NAMEDAY_LIST) as f:
    #with open(NAMEDAY_LIST, "r", encoding="utf-8") as f:
        namedays = json.load(f)

    return namedays

def print_namedays(date_str):

    namedays = read_namedays()

    if date_str in namedays:
        nameday = namedays[date_str]
        print(f"Šodienas vārda dienas: {", ".join(nameday)}")
    else:
        print("Šodien nav neviena vārda diena.")

    print()

def get_date_for_name(name):

    namedays = read_namedays()

    # Search for the name in the calendar
    for date, names in namedays.items():
        if name in names:
            return date
    return None

def print_nameday_for_name(name):
    
    date = get_date_for_name(name)

    if date:
        print(f"{name}: vārda diena ir {date} (MM-DD)")
    else:
        print(f"Nevarēju atrast vārda dienu: {name}")

    print()

def main():

    # TODO:
    #  - Print today's names if no arguments are given
    #  - Print the name day for a specific name if the program has 1 (or more?) argument(s)
    #  - Print help if the program has the --help argument
    #  - Create library functions for nameday lookup

    parser = argparse.ArgumentParser(description="Latvian name day lookup")
    parser.add_argument("--today", action="store_true", help="Show today's name days")
    parser.add_argument("--name", type=str, help="Look up a name day for a specific name")

    args = parser.parse_args()

    if args.today:
        print_namedays(dt.datetime.now().strftime("%m-%d"))

    elif args.name:
        date = print_nameday_for_name(args.name.strip())

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
