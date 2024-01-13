"""Main Module."""

import re
from pathlib import Path

from genderize import Genderize


def main() -> None:
    """Execute main function."""
    years_with_register = list(range(2011, 2022 + 1))

    # collect all names
    all_years_names = []
    for year in years_with_register:
        filepath = Path(f"chronological-registers/{year}.txt")
        fulltext = filepath.read_text()
        author_names_raw = re.findall(r"\((\D*)\)", fulltext)
        single_author_names = list(filter(lambda name: "/" not in name, author_names_raw))
        # multiple_author_names = list(filter(lambda name: "/" in name, author_names_raw))
        single_author_first_names = [name.split(" ")[0] for name in single_author_names]
        all_years_names.extend(single_author_first_names)

    # Sample
    sample_names = all_years_names[:10]  # 10 names maximum per call

    # analyze names via https://genderize.io/
    genderize_api_response = Genderize().get([sample_names])
    genders = [ item["gender"] for item in genderize_api_response ] # pyright: ignore [reportGeneralTypeIssues]

    # calculate percentage
    total = len(sample_names)
    percentage_females = str(genders.count("female") / total * 100) + "%"
    print(f"In Sample: {percentage_females = }")


if __name__ == "__main__":
    main()
