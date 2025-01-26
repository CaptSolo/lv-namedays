import datetime as dt
import click

from .nameday import read_namedays, get_date_for_name

@click.group()
def cli():
    """
    A program for lookup in the Latvian name day calendar.

    It can display today's name days and look up the name day date
    for a specific name.
    """
    pass

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
        nameday_lst = ", ".join(nameday) 
        click.echo(f"{msg} {nameday_lst}")
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

            nameday_lst = ", ".join(nameday)
            click.secho(f"{date_str} vārda dienas: {nameday_lst}", bold=bold)
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
