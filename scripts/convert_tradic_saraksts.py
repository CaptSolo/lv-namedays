"""
Program for converting the official namesday list from the Latvian
language center into a JSON file. The list is in the form of an Excel
file, which is converted to a JSON file.

Input data: 
https://data.gov.lv/dati/lv/dataset/latviesu-tradicionalais-un-paplasinatais-kalendarvardu-saraksts
"""

import pandas as pd
import csv
import json

BASIC_FILENAME = "tradic_vardadienu_saraksts.xlsx"
BASIC_CSV = "tradic_vardadienu_saraksts.csv"
BASIC_OUTPUT = "tradic_vardadienu_saraksts.json"

def convert_basic_list():

    basic_df = pd.read_excel(BASIC_FILENAME)
    basic_df.to_csv(BASIC_CSV, index=False, header=False)

    dataset = {}

    with open(BASIC_CSV) as inf:

        csv_in = csv.reader(inf)

        for rec in csv_in:

            if len(rec) != 2:
                break

            date_str, names_str = rec
            day, month = date_str.split(".")[:2]
            date = f"{month}-{day}"

            names_str = names_str.replace(".", ",")
            names = names_str.split(",")
            names = [text.strip() for text in names]

            dataset[date] = names

    with open(BASIC_OUTPUT, "w") as outf:

        json.dump(dataset, outf, indent=2)


def main():
    
    convert_basic_list()

if __name__ == "__main__":
    main()