# Latvian name day list (vārda dienu saraksts)

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

### Usage - command line

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

### Usage - as a library

The name day lookup functionality can also be imported and used as a library:

```python
from lv_namedays import NameDayDB

db = NameDayDB()

# Look up the name day for Uldis (4th of July)
db.get_date_for_name("Uldis")
>>> '07-04'

# Look up the names for the 1st of July
db.get_names_for_date("07-01")
>>> ['Imants', 'Rimants', 'Ingars', 'Intars']

# Get the full name days list (dictionary)
db.namedays
>>> {'01-01': ['Laimnesis', 'Solvita', 'Solvija'], ..., '12-31': ['Silvestrs', 'Silvis', 'Kalvis']}
```

### Data source

https://data.gov.lv/dati/eng/dataset/latviesu-tradicionalais-un-paplasinatais-kalendarvardu-saraksts

### Related projects

- [slikts/vardadienas](https://github.com/slikts/vardadienas)
- [laacz: namedays](https://gist.github.com/laacz/5cccb056a533dffb2165)
