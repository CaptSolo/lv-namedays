#!/usr/bin/env python3

"""
A program for working with the Latvian name day calendar.

It can display today's name days and look up the name day date
for a specific name.
"""

import datetime as dt
import json
import argparse
import os
import importlib.resources
import click


NAMEDAY_LIST = "tradic_vardadienu_saraksts.json"

@click.group()
def cli():
    """
    A program for lookup in the Latvian name day calendar.

    It can display today's name days and look up the name day date
    for a specific name.
    """
    pass

def read_namedays():

    with importlib.resources.open_text('lv_namedays.data', NAMEDAY_LIST) as f:
    #with open(NAMEDAY_LIST, "r", encoding="utf-8") as f:
        namedays = json.load(f)

    return namedays

@cli.command()
def now():
    """
    Show today's name days.
    """
    print_namedays(dt.datetime.now().strftime("%m-%d"))

def print_namedays(date_str):
    
    namedays = read_namedays()

    click.echo()

    if date_str in namedays:
        nameday = namedays[date_str]
        click.echo(f"Šodienas vārda dienas: {", ".join(nameday)}")
    else:
        click.echo("Šodien nav neviena vārda diena.")

    click.echo()

def get_date_for_name(name):

    namedays = read_namedays()

    # Search for the name in the calendar
    for date, names in namedays.items():
        if name in names:
            return date
    return None

@cli.command()
@click.argument("name")
def name(name):
    """
    Show the name day for a specific name.
    """
    print_nameday_for_name(name)


def print_nameday_for_name(name):
    
    date = get_date_for_name(name)

    click.echo()

    if date:
        click.echo(f"{name}: vārda diena ir {date} (MM-DD)")
    else:
        click.echo(f"Nevarēju atrast vārda dienu: {name}")

    click.echo()

def main():

    cli()

    # TODO:
    #  - Print today's names if no arguments are given
    #  - Print the name day for a specific name if the program has 1 (or more?) argument(s)
    #  - Print help if the program has the --help argument
    #  - Create library functions for nameday lookup

    #parser = argparse.ArgumentParser(description="Latvian name day lookup")
    #parser.add_argument("--today", action="store_true", help="Show today's name days")
    #parser.add_argument("--name", type=str, help="Look up a name day for a specific name")

if __name__ == "__main__":
    main()
