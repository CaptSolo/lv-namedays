#!/usr/bin/env python3

"""
A program for working with the Latvian name day calendar.

It can display today's name days and look up the name day date
for a specific name.
"""

import datetime as dt
import json
import importlib.resources
from importlib.resources import files
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
    """Read the name day data from the JSON file."""

    data_path = files('lv_namedays.data').joinpath(NAMEDAY_LIST)
    
    with data_path.open('r', encoding='utf-8') as f:
        namedays = json.load(f)

    return namedays


@cli.command()
def now():
    """
    Show today's name days.
    """
    print_namedays(dt.datetime.now().strftime("%m-%d"))

def print_namedays(date_str, msg=None):
    
    namedays = read_namedays()

    click.echo()

    if not msg:
        msg = "Šodienas vārda dienas:"

    if date_str in namedays:
        nameday = namedays[date_str]
        click.echo(f"{msg} {", ".join(nameday)}")
    else:
        click.echo("Šodien nav neviena vārda diena.")

    click.echo()

@cli.command()
@click.argument("date")
def date(date: str) -> None:
    """
    Show name days for a specific date (in MM-DD format).
    """
    if len(date) != 5 or date[2] != "-":
        click.echo("Incorrect date format. Enter date in MM-DD format.")
        return

    month, day = date.split("-")
    try:
        dt.datetime(2000, int(month), int(day))
    except ValueError:
        click.echo("Incorrect date format. Enter a correct date in MM-DD format.")
        return

    print_namedays(date, msg=f"{date} vārda dienas:")

def get_date_for_name(name):

    namedays = read_namedays()

    # Make search case insensitive
    namedays = {date: [n.lower() for n in names] for date, names in namedays.items()}

    # Search for the name in the calendar
    for date, names in namedays.items():
        if name.lower() in names:
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


def print_namedays_for_week(date):

    start_date = date - dt.timedelta(days=3)

    namedays = read_namedays()

    click.echo()

    for i in range(7):
        current_date = start_date + dt.timedelta(days=i)
        date_str = current_date.strftime("%m-%d")

        if date_str in namedays:
            nameday = namedays[date_str]

            bold = False

            if current_date == date:
                bold = True

            click.secho(f"{date_str} vārda dienas: {", ".join(nameday)}", bold=bold)
        else:
            click.echo(f"{date_str} nav neviena vārda diena")

    click.echo()

@cli.command()
def week():
    """
    Show name days for the current day and 3 days before and after it.
    """

    date = dt.datetime.now().date()
    print_namedays_for_week(date)

def main():

    cli()

    # TODO:
    #  - Create library functions for nameday lookup

if __name__ == "__main__":
    main()
