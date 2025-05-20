import datetime as dt
import click

from .nameday import NameDayDB

@click.group()
def cli():
    """
    A program for lookup in the Latvian name day calendar.

    It can display today's name days and look up the name day date
    for a specific name.
    """
    pass

@cli.command()
@click.option("-e", "--extended", is_flag=True, help="Use the extended name day list.")
def now(extended: bool) -> None:
    """
    Show today's name days.
    """
    print_namedays(dt.datetime.now().strftime("%m-%d"), extended=extended)

def print_namedays(date_str, msg=None, extended=False):
    
    db = NameDayDB()

    click.echo()

    if not msg:
        msg = "Šodienas vārda dienas:"

    names = db.get_names_for_date(date_str, extended=extended)
    
    if names is not None:
        nameday_lst = ", ".join(names) 
        click.echo(f"{msg} {nameday_lst}")
    else:
        click.echo("Nav informācija par vārda dienām šajā datumā.")

    click.echo()

@cli.command()
@click.argument("date")
@click.option("-e", "--extended", is_flag=True, help="Use the extended name day list.")
def date(date: str, extended: bool) -> None:
    """
    Show name days for a specific date (in MM-DD format).
    """
    if len(date) != 5 or date[2] != "-":
        click.echo("Nepareizs datums. Ievadiet datumu MM-DD formātā.")
        return

    month, day = date.split("-")

    try:
        dt.datetime(2000, int(month), int(day))
    except ValueError:
        click.echo("Nepareizs datums. Ievadiet datumu MM-DD formātā.")
        return

    print_namedays(date, msg=f"{date} vārda dienas:", extended=extended)

@cli.command()
@click.argument("name")
def name(name):
    """
    Show the name day for a specific name.
    """
    print_nameday_for_name(name)

def print_nameday_for_name(name):

    db = NameDayDB()

    click.echo()

    if date := db.get_date_for_name(name):
        click.echo(f"{name}: vārda diena ir {date} (MM-DD)")
    elif date := db.get_date_for_name(name, extended=True):
        click.echo(f"{name}: vārda diena (paplašinātajā sarakstā) ir {date} (MM-DD)")
    else:
        click.echo(f"Nevarēju atrast vārda dienu: {name}")

    click.echo()


def print_namedays_for_week(date):

    start_date = date - dt.timedelta(days=3)

    db = NameDayDB()

    click.echo()

    for i in range(7):
        current_date = start_date + dt.timedelta(days=i)
        date_str = current_date.strftime("%m-%d")

        names = db.get_names_for_date(date_str)

        if names is not None:

            bold = False

            if current_date == date:
                bold = True

            nameday_lst = ", ".join(names)
            click.secho(f"{date_str} vārda dienas: {nameday_lst}", bold=bold)

    click.echo()

@cli.command()
def week():
    """
    Show name days for the current day and 3 days before and after it.
    """

    date = dt.datetime.now().date()
    print_namedays_for_week(date)
