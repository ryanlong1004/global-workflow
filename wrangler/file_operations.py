import csv
from pathlib import Path
from typing import Any
import pandas


def write_to_csv(output_path: Path, data: Any, fieldnames=[]):
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        spamwriter = csv.DictWriter(
            csvfile,
            delimiter=",",
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL,
            fieldnames=fieldnames,
        )
        spamwriter.writeheader()
        for item in data:
            spamwriter.writerow(dict(zip(fieldnames, item)))


def read_from_csv(input_path: Path):
    with open(input_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)


def read_csv_into_dataframe(filename: str) -> pandas.DataFrame:
    return pandas.read_csv(filename, index_col=0, header=0)


def get_modules_and_jobs(df: pandas.DataFrame) -> tuple:
    modules = df.columns.tolist()
    jobs = df.index.tolist()
    return (modules, jobs)


def get_list_of_columns_given_row(df: pandas.DataFrame, row_name: str) -> list:
    row = df.loc[row_name]
    column = list(row[row.notna()].index)
    return column


if __name__ == "__main__":
    pass
