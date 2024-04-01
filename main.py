"""Main Module."""

from __future__ import annotations

import re
from pathlib import Path
from typing import TypedDict

from genderize import Genderize


def main() -> None:
    """Execute main function."""
    all_years_names = get_all_names_from_raw_data()
    check_sample_data(all_years_names)


def check_sample_data(data: list[str]) -> None:
    """Inspect a sample.

    Creates sample of 10 names from the input data with the genderize API.
    Prints percentage of females in the sample.
    """
    sample_names = data[:10]  # 10 names maximum per call

    # analyze names via https://genderize.io/
    genderize_api_response = Genderize().get(sample_names)
    genders = [item["gender"] for item in genderize_api_response]

    # calculate percentage
    total = len(sample_names)
    percentage_females = str(genders.count("female") / total * 100) + "%"
    print(f"{percentage_females = }\n(in sample)")


def get_all_names_from_raw_data() -> list[str]:
    """Gets all names from raw data (chronological-registers).

    currently:
    - only single authors, for 2011 - 2022
    - simple list, containing duplicates
    - contains some non-names/wrong reading from raw-data (TODO: remove those)
    """
    years_with_register = list(range(2011, 2022 + 1))

    # collect all  names
    all_years_names: list[str] = []
    for year in years_with_register:
        filepath = Path(f"chronological-registers/{year}.txt")
        fulltext = filepath.read_text()
        author_names_raw = re.findall(r"\((\D*)\)", fulltext)
        single_author_names = list(filter(lambda name: "/" not in name, author_names_raw))
        # multiple_author_names = list(filter(lambda name: "/" in name, author_names_raw))
        single_author_first_names = [name.split(" ")[0] for name in single_author_names]
        all_years_names.extend(single_author_first_names)
    return all_years_names


def calc_gender_dist_in_dataset(list_of_names: list[str]) -> float:
    """Calculates the gender distribution in the dataset."""
    return 0.5


# ──────────────────────────────────────────────────────────────────────────────


def fetch_gender_into_caching_db() -> None:
    """Fetches gender from into our local database.

    Gets all names in Database with missing gender, and creates batches to call
    via the genderize API. Saves the results in our local database.
    """


def lookup_name_in_caching_db(name_to_check: str) -> str | None:
    """Looks a name in our local database (as hashmap to avoid duplicates).

    Given a name, returns "male" or "female" if the name is in the database.
    If not, adds the name to the database with no gender, and returns None.
    """

    class CacheDatabaseEntry(TypedDict):
        name: str
        gender: str
        probability: float

    # 1. check if cache exists, if not, create cache database as csv with header
    location_of_cache_db = "./databases/"
    parent_dir = Path(location_of_cache_db)
    if not parent_dir.exists():
        parent_dir.mkdir()

    filename_of_cache_db = "cache.csv"
    path_of_cache_db = location_of_cache_db + filename_of_cache_db
    cache_db = Path(path_of_cache_db)
    if not cache_db.exists():
        cache_db.touch()  # touch = create empty file

    # 2. check if name is in cache
    cache_content = cache_db.read_text()
    data_rows = cache_content.strip().split("\n")
    cache_db_entries: list[CacheDatabaseEntry] = []
    num_of_columns = 3
    for row in data_rows:
        parts = row.strip().split(";")
        if len(parts) != num_of_columns:  # in case csv-row has insufficient semicolons
            continue
        name, gender, probability = parts
        cache_db_entries.append(
            {
                "name": name,
                "gender": gender,
                "probability": float(probability),
            },
        )

    # 2a. if name is in cache, return gender (and probability)
    for entry in cache_db_entries:
        if entry["name"] == name_to_check:
            return f"gender: {entry["gender"]}, probability: {entry["probability"]}"

    # 2b. if name is not in cache, then add name to cache with no gender and
    # return None
    new_csv_row = f"{name_to_check};undetermined;-1"
    cache_db.open("a").write(new_csv_row + "\n")
    return None


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    output = lookup_name_in_caching_db("Tonia")  
    print(output)
