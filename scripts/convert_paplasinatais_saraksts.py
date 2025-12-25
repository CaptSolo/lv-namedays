"""
Program for converting the official extended namesday list from the 
Latvian language center into a JSON file. The list is in the form 
of a CSV file, which this script converts to a JSON file.

Input data: 
https://www.vvc.gov.lv/lv/kalendarvardu-ekspertu-komisija
"""

import pandas as pd
import csv
import json

EXTENDED_CSV = "Paplašinātais vārdadienu saraksts.csv"
EXTENDED_OUTPUT = "paplasinatais_saraksts.json"

def convert_extended_list():

    dataset = {}

    with open(EXTENDED_CSV) as inf:

        csv_in = csv.reader(inf, delimiter=";")

        # Skip the header row
        next(csv_in)

        for rec in csv_in:

            if len(rec) != 2:
                break

            date_str, names_str = rec

            # Skip incorrect dates (if any)
            if len(date_str.split(".")) < 2:
                continue

            day, month = date_str.split(".")[:2]

            date = f"{month}-{day}"

            has_name_day = False

            if "Visu neparasto un kalendāros neierakstīto vārdu diena " in names_str:
                names_str = names_str.replace("Visu neparasto un kalendāros neierakstīto vārdu diena ", "")
                has_name_day = True

            names_str = names_str.replace("(LTG: ", "")
            names_str = names_str.replace(")", "")

            names_str = names_str.replace(".", ",")
            names_str = names_str.replace(" ", ",")

            names = names_str.split(",")
            # Also removes "–" from the list
            names = [text.strip() for text in names if text != "–" and text != ""]

            if has_name_day:
                names.append("Visu neparasto un kalendāros neierakstīto vārdu diena")

            dataset[date] = names

    with open(EXTENDED_OUTPUT, "w") as outf:
        json.dump(dataset, outf, indent=2)


def main():
    
    convert_extended_list()

if __name__ == "__main__":
    main()
