import csv
from pathlib import Path
from typing import Any


def write_to_csv(output_path: Path, data: Any):
    with open(output_path, "w", newline="") as csvfile:
        for item in data:
            spamwriter = csv.writer(
                csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            item = [item] if isinstance(item, str) else item
            spamwriter.writerow([*(item)])
