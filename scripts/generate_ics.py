#!/usr/bin/env python3
"""
Generate an .ics (iCalendar) file from the Latvian name day list.

This script reads the traditional name day list JSON file and creates
an iCalendar file that can be imported into calendar applications like
Google Calendar, Apple Calendar, Outlook, etc.

Each name day is created as an all-day recurring event that repeats yearly.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def escape_ics_text(text):
    """
    Escape special characters for iCalendar format.
    According to RFC 5545, backslash, semicolon, and comma need to be escaped.
    """
    text = text.replace('\\', '\\\\')
    text = text.replace(',', '\\,')
    text = text.replace(';', '\\;')
    text = text.replace('\n', '\\n')
    return text


def generate_ics(json_file, output_file, year=2026):
    """
    Generate an iCalendar file from the name day JSON data.

    Args:
        json_file: Path to the JSON file with name day data
        output_file: Path where the .ics file will be written
        year: Base year to use for date generation (default: 2026)
    """
    # Read the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        namedays = json.load(f)

    # Start building the ICS content
    ics_lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Latvian Name Days//lv-namedays//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'X-WR-CALNAME:Vārda dienas',
        'X-WR-TIMEZONE:Europe/Riga',
        'X-WR-CALDESC:Latviešu vārda dienu kalendārs',
    ]

    # Current timestamp for DTSTAMP
    now = datetime.now(timezone.utc)
    dtstamp = now.strftime('%Y%m%dT%H%M%SZ')

    # Counter for events created
    event_count = 0

    # Process each date
    for date_key, names in sorted(namedays.items()):
        # Skip leap day placeholder
        if names == ['-']:
            continue

        # Parse the date
        month, day = date_key.split('-')

        # Skip invalid dates (like Feb 29 in non-leap years)
        try:
            event_date = datetime(year, int(month), int(day))
        except ValueError:
            continue

        # Format the date for DTSTART (YYYYMMDD format for all-day events)
        dtstart = event_date.strftime('%Y%m%d')

        # Calculate end date (next day)
        from datetime import timedelta
        dtend = (event_date + timedelta(days=1)).strftime('%Y%m%d')

        # Create the event summary
        names_str = ', '.join(names)
        summary = names_str

        # Create a unique UID for this event
        uid = f'nameday-{date_key}@lv-namedays'

        # Add the event
        ics_lines.extend([
            'BEGIN:VEVENT',
            f'DTSTART;VALUE=DATE:{dtstart}',
            f'DTEND;VALUE=DATE:{dtend}',
            f'DTSTAMP:{dtstamp}',
            f'UID:{uid}',
            f'SUMMARY:{escape_ics_text(summary)}',
            'URL:https://github.com/CaptSolo/lv-namedays',
            'RRULE:FREQ=YEARLY',
            'TRANSP:TRANSPARENT',
            'STATUS:CONFIRMED',
            'SEQUENCE:0',
            'END:VEVENT',
        ])

        event_count += 1

    # Close the calendar
    ics_lines.append('END:VCALENDAR')

    # Write to file with proper line endings (CRLF as per RFC 5545)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\r\n'.join(ics_lines))

    print(f'Generated {output_file} with {event_count} name day events')


def main():
    # Determine paths relative to the script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Input JSON file
    json_file = project_root / 'src' / 'lv_namedays' / 'data' / 'tradic_vardadienu_saraksts.json'

    # Output ICS file
    output_file = 'latvian_namedays.ics'

    if not json_file.exists():
        print(f'Error: Input file not found: {json_file}')
        return 1

    generate_ics(json_file, output_file)
    print(f'Successfully created: {output_file}')

    return 0


if __name__ == '__main__':
    exit(main())
