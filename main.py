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


class CacheDatabaseEntry(TypedDict):
    """Entry in the cache database."""

    name: str
    gender: str
    probability: float


def csv_to_cache_db(cache_db: Path) -> list[CacheDatabaseEntry]:
    """Converts csv to cache database."""
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
    return cache_db_entries


def fetch_gender_into_caching_db() -> None:
    """Fetches gender from into our local database.

    Gets all names in Database with undetermined gender, and creates batches to call
    via the genderize API. Saves the results in our local database.
    """
    # 1. get 10 undetermined names
    location_of_cache_db = "./databases/cache.csv"
    cache_db = Path(location_of_cache_db)
    if not cache_db.exists():
        print("Cache does not exist yet.")
        return

    cache_db_entries = csv_to_cache_db(cache_db)
    entries_without_gender = filter(
        lambda entry: entry["gender"] == "undetermined",
        cache_db_entries,
    )
    names_only = [entry["name"] for entry in entries_without_gender]

    # DOCS https://genderize.io/faq#api-usage
    names_per_call = 10
    calls_per_day_free_tier = 100
    max_names_to_fetch = names_per_call * calls_per_day_free_tier

    acc_genderize_response: list[dict[str, str|float]] = []
    for i in range(0, max_names_to_fetch, names_per_call):
        chunk = names_only[i:(i + names_per_call)]
        response = Genderize().get(chunk)
        acc_genderize_response.extend(response)

    # 2. update cache (NOTE performance can be improved)
    for response_item in acc_genderize_response:
        for cache_entry in cache_db_entries:
            if cache_entry["name"] == response_item["name"]:
                cache_entry["gender"] = str(response_item["gender"])
                cache_entry["probability"] = float(response_item["probability"])
                break

    # 3. write cache back to csv
    csv_text = ""
    for entry in cache_db_entries:
        row = f"{entry["name"]};{entry["gender"]};{entry["probability"]}\n"
        csv_text += row

    cache_db.write_text(csv_text)
    print("Updated cache with new names.")


def lookup_name_in_caching_db(name_to_check: str) -> str | None:
    """Looks a name in our local database (as hashmap to avoid duplicates).

    Given a name, returns "male" or "female" if the name is in the database.
    If not, adds the name to the database with no gender, and returns None.
    """
    # 1. check if cache exists, if not, create cache database as csv
    location_of_cache_db = "./databases/"
    parent_dir = Path(location_of_cache_db)
    if not parent_dir.exists():
        parent_dir.mkdir()

    filename_of_cache_db = "cache.csv"
    path_of_cache_db = location_of_cache_db + filename_of_cache_db
    cache_db = Path(path_of_cache_db)
    if not cache_db.exists():
        cache_db.touch()  # touch = create empty file

    # 2. read entries
    cache_db_entries = csv_to_cache_db(cache_db)

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
    fetch_gender_into_caching_db()
