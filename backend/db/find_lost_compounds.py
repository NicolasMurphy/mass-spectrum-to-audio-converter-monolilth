import json


def find_lost_compounds(old_file, new_file):
    """
    List compounds that are in the old file but not in the new file
    """

    try:
        with open(old_file, "r", encoding="utf-8") as f:
            old_compounds = set(json.load(f))
    except Exception as e:
        print(f"Error loading old file: {e}")
        return

    try:
        with open(new_file, "r", encoding="utf-8") as f:
            new_compounds = set(json.load(f))
    except Exception as e:
        print(f"Error loading new file: {e}")
        return

    lost_compounds = old_compounds - new_compounds

    print(f"Total compounds lost: {len(lost_compounds)}")
    print(f"\nCompounds in old file but not in new file:")
    print("=" * 50)

    for compound in sorted(lost_compounds):
        print(compound)


if __name__ == "__main__":
    old_file = "compounds_old.json"
    new_file = "compounds_new.json"

    find_lost_compounds(old_file, new_file)
