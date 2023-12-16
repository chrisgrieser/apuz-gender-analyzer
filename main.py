"""Main Module."""


from pathlib import Path


def main() -> None:
    """Execute main function."""
    # years_with_register = list(range(2011, 2022 + 1))
    # for year in years_with_register:
    #     print(f"Register for {year} is available.")
    filepath = Path("chronological-registers/2011.txt")
    text = filepath.read_text()
    find = text.find("Mouffe")
    print(f"🪚 {find = }")


if __name__ == "__main__":
    main()
