# Latvian name day list

This repository contains the Latvian name day list and an utility for working with it.

About [Latvian name days](https://en.wikipedia.org/wiki/Name_day#Latvia)

### Installation

To install this tool from Github run:

```
pip install -U "git+https://github.com/CaptSolo/lv-namedays"
```

Using `uv`:

```
uv pip install -U "git+https://github.com/CaptSolo/lv-namedays"
```

You can also run it directly without installing by using `uvx`:

```
uvx --from "git+https://github.com/CaptSolo/lv-namedays" nameday
```

### Usage

```
Usage: nameday [OPTIONS] COMMAND [ARGS]...

  A program for lookup in the Latvian name day calendar.

  It can display today's name days and look up the name day date for a
  specific name.

Options:
  --help  Show this message and exit.

Commands:
  name  Show the name day for a specific name.
  now   Show today's name days.
  week  Show name days for the current day and 3 days before and after it.
```

### Data source

https://data.gov.lv/dati/eng/dataset/latviesu-tradicionalais-un-paplasinatais-kalendarvardu-saraksts

### Related projects

- [slikts/vardadienas](https://github.com/slikts/vardadienas)
- [laacz: namedays](https://gist.github.com/laacz/5cccb056a533dffb2165)
