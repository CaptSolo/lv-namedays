# Latvian name day list (vārda dienu saraksts)

*Updated with new name day lists for 2026.*

This repository contains the Latvian name day list and an utility for working with it.

About [Latvian name days](https://en.wikipedia.org/wiki/Name_day#Latvia).

### Installation

To install this tool run:

```
pip install lv-namedays
```

Using `uv`:

```
uv pip install lv-namedays
```

You can also install it as a `uv` tool and then run it directly from shell:

```
> uv tool install lv-namedays

> nameday now

Šodienas vārda dienas: Antons, Antis, Antonijs
```

### Usage - summary

```
Usage: nameday [OPTIONS] COMMAND [ARGS]...

  A program for lookup in the Latvian name day calendar.

  It can display today's name days and look up the name day date for a
  specific name.

Options:
  --help  Show this message and exit.

Commands:
  date  Show name days for a specific date (in MM-DD format).
  name  Show the name day for a specific name.
  now   Show today's name days.
  week  Show name days for the current day and 3 days before and after it.
```

### Usage - as a command-line tool

#### Get the names for a given date

```
❯ nameday date 07-23

07-23 vārda dienas: Magda, Magone, Mērija, Magdalēna
```

You can also look up names in the extended name day list by supplying the `-e` or `--extended` option:

```
❯ nameday date 07-23 --extended

07-23 vārda dienas: Magda, Magone, Mērija, Magdalēna, Madelaina, Madeleina, Madlena, Madlēna, Magdalena, Magdaliene, Magdalina, Magita, Meralda, Meri, Merīda, Merija, Merilina, Merita, Radislavs, Radmila, Radomirs
```

You can also ask for today's names (the `-e` or `--extended` option can be used here, too):

```
❯ nameday now

Šodienas vārda dienas: Venta, Salvis, Selva
```

#### Get the name day for a given name

Find the name day date for a given name:

```
❯ nameday name Uldis

Uldis: vārda diena ir 07-04 (MM-DD)
```

This command also looks up names in the extended name day list:

```
❯ nameday name Radomirs

Radomirs: vārda diena (paplašinātajā sarakstā) ir 07-23 (MM-DD)
```

#### Show name days for a week

Use the `week` command to display names for a week (the current date +/- 3 days):

```
❯ nameday week

05-17 vārda dienas: Herberts, Dailis, Umberts
05-18 vārda dienas: Inese, Inesis, Ēriks
05-19 vārda dienas: Lita, Sibilla, Teika
05-20 vārda dienas: Venta, Salvis, Selva
05-21 vārda dienas: Ernestīne, Ingmārs, Akvelīna
05-22 vārda dienas: Emīlija, Visu neparasto un kalendāros neierakstīto vārdu diena
05-23 vārda dienas: Leontīne, Leokādija, Lonija, Ligija
```

### Usage - as a library

The name day lookup functionality can also be imported and used as a library:

```python
from lv_namedays import NameDayDB

db = NameDayDB()

# Look up the name day for Uldis (4th of July)
db.get_date_for_name("Uldis")
>>> '07-04'

# Look up the name day in the extended name day list
db.get_date_for_name("Radomirs", extended=True)
>>> '07-23'

# Look up the names for the 1st of July
db.get_names_for_date("07-01")
>>> ['Imants', 'Rimants', 'Ingars', 'Intars']

# Look up the names in the extended name day list
db.get_names_for_date("07-01", extended=True)
>>> ['Imants', 'Rimants', 'Ingars', 'Intars', 'Ingārs', 'Ingera', ...]
```

You can also access the full list of name days (both the core and the extended name day list) that this application is using:

```
# Get the core name days list (dictionary)
db.namedays
>>> {'01-01': ['Laimnesis', 'Solvita', 'Solvija'], ..., '12-31': ['Silvestrs', 'Silvis', 'Kalvis']}

# Get the extended name days list (dictionary)
db.namedays_ext
>>> {'01-01': ['Laimnesis', 'Solvita', 'Solvija', 'Afra', 'Afrodīte', ...], ...}
```

### Testing

Check out this code with the `dev` dependency group.

Then run `pytest`

In order to test this app with different python versions run `tox`

### Data source

https://www.vvc.gov.lv/lv/kalendarvardu-ekspertu-komisija

### Related projects

- [slikts/vardadienas](https://github.com/slikts/vardadienas)
- [laacz: namedays](https://gist.github.com/laacz/5cccb056a533dffb2165)
