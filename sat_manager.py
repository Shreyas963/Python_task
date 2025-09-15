#!/usr/bin/env python3
"""
SAT Results Manager
Features:
1. Insert data
2. View all data (JSON)
3. Get rank
4. Update score
5. Delete one record
6. Calculate Average SAT Score
7. Filter records by Pass/Fail
8. Put the inserted data in json format in a file (explicit save)
Extra: 9. Exit

Data is persisted to 'sat_data.json'. The script asks for a maximum SAT score on first run (default 100).
Note: pass/fail is computed as score > 30% of the configured max score.

# hatchling
"""

import json
import os
import sys

DATA_FILE = "sat_data.json"


def load_data(filename=DATA_FILE):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # If file corrupt, start fresh
            data = {"max_score": 100, "records": {}}
    else:
        data = {"max_score": 100, "records": {}}
    # Ensure keys
    if "max_score" not in data:
        data["max_score"] = 100
    if "records" not in data:
        data["records"] = {}
    return data


def save_data(data, filename=DATA_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[Saved] Data written to {filename}")


def compute_pass(score, max_score):
    try:
        s = float(score)
    except Exception:
        return False
    return s > 0.3 * float(max_score)


def insert_data(data):
    print("\n--- Insert New Candidate ---")
    name = input("Name (unique identifier): ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if name in data["records"]:
        print("A record with this name already exists.")
        return

    address = input("Address: ").strip()
    city = input("City: ").strip()
    country = input("Country: ").strip()
    pincode = input("Pincode: ").strip()

    # SAT score input and validation
    while True:
        score_inp = input(f"SAT score (numeric, max {data['max_score']}): ").strip()
        try:
            score = float(score_inp)
            break
        except ValueError:
            print("Please enter a valid numeric score.")

    passed = compute_pass(score, data["max_score"])

    record = {
        "name": name,
        "address": address,
        "city": city,
        "country": country,
        "pincode": pincode,
        "sat_score": score,
        "passed": passed,
    }

    data["records"][name] = record
    save_data(data)


def view_all_data(data):
    print("\n--- All Records (JSON) ---")
    if not data["records"]:
        print("No records available.")
        return
    print(json.dumps({"max_score": data["max_score"], "records": data["records"]}, indent=2, ensure_ascii=False))


def get_rank(data):
    print("\n--- Get Rank by Name ---")
    if not data["records"]:
        print("No records to rank.")
        return
    name = input("Enter candidate name: ").strip()
    if name not in data["records"]:
        print("Candidate not found.")
        return
    my_score = float(data["records"][name]["sat_score"])
    all_scores = [float(r["sat_score"]) for r in data["records"].values()]

    # Rank = 1 + number of people with strictly higher score
    higher_count = sum(1 for s in all_scores if s > my_score)
    rank = 1 + higher_count
    # Also compute total candidates and total with same score
    same_score_count = sum(1 for s in all_scores if s == my_score)
    total = len(all_scores)
    print(f"{name} -> Score: {my_score}, Rank: {rank} (out of {total}).")
    if same_score_count > 1:
        print(f"Note: {same_score_count} candidate(s) have the same score.")


def update_score(data):
    print("\n--- Update Candidate SAT Score ---")
    if not data["records"]:
        print("No records to update.")
        return
    name = input("Enter candidate name to update: ").strip()
    if name not in data["records"]:
        print("Candidate not found.")
        return
    while True:
        new_score_inp = input(f"New SAT score (numeric, max {data['max_score']}): ").strip()
        try:
            new_score = float(new_score_inp)
            break
        except ValueError:
            print("Please enter a valid numeric score.")

    data["records"][name]["sat_score"] = new_score
    data["records"][name]["passed"] = compute_pass(new_score, data["max_score"])
    save_data(data)
    print("Score updated.")


def delete_one_record(data):
    print("\n--- Delete One Record ---")
    if not data["records"]:
        print("No records to delete.")
        return
    name = input("Enter candidate name to delete: ").strip()
    if name not in data["records"]:
        print("Candidate not found.")
        return
    confirm = input(f"Type 'yes' to confirm deletion of '{name}': ").strip().lower()
    if confirm == "yes":
        del data["records"][name]
        save_data(data)
        print("Record deleted.")
    else:
        print("Deletion cancelled.")


def calculate_average(data):
    print("\n--- Average SAT Score ---")
    if not data["records"]:
        print("No records.")
        return
    scores = [float(r["sat_score"]) for r in data["records"].values()]
    avg = sum(scores) / len(scores)
    print(f"Average SAT score ({len(scores)} candidates): {avg:.2f} / {data['max_score']}")


def filter_by_pass_fail(data):
    print("\n--- Filter Records by Pass/Fail ---")
    if not data["records"]:
        print("No records.")
        return
    choice = input("Enter 'pass' to show passed, 'fail' to show failed: ").strip().lower()
    if choice not in ("pass", "fail"):
        print("Invalid choice.")
        return
    want_pass = choice == "pass"
    results = [r for r in data["records"].values() if r.get("passed") == want_pass]
    if not results:
        print(f"No {choice} records.")
        return
    print(json.dumps(results, indent=2, ensure_ascii=False))


def explicit_save(data):
    print("\n--- Save Data to JSON File ---")
    save_data(data)


def set_max_score(data):
    print(f"\nCurrent max score: {data['max_score']}")
    while True:
        new_max = input("Enter new maximum SAT score (leave blank to keep current): ").strip()
        if new_max == "":
            print("Max score unchanged.")
            return
        try:
            nm = float(new_max)
            if nm <= 0:
                print("Please enter a positive number.")
                continue
            data["max_score"] = nm
            # Recompute pass flags for all records
            for rec in data["records"].values():
                rec["passed"] = compute_pass(rec["sat_score"], data["max_score"])
            save_data(data)
            print(f"Max score updated to {nm} and pass/fail re-evaluated.")
            return
        except ValueError:
            print("Please enter a valid number.")


def menu_loop():
    data = load_data()
    # If first run and default max_score, ask the user if they'd like to change it
    if data.get("max_score", 100) == 100 and not data["records"]:
        print("No data found. Default max score is 100. You can change this later.")
    while True:
        print("\n--- SAT Manager Menu ---")
        print("1. Insert data")
        print("2. View all data")
        print("3. Get rank")
        print("4. Update score")
        print("5. Delete one record")
        print("6. Calculate Average SAT Score")
        print("7. Filter records by Pass/Fail Status")
        print("8. Put the inserted data in JSON file (explicit save)")
        print("9. Exit")
        print("10. (Optional) Set max SAT score (current: {})".format(data.get("max_score")))
        choice = input("Choose an option (1-10): ").strip()
        if choice == "1":
            insert_data(data)
        elif choice == "2":
            view_all_data(data)
        elif choice == "3":
            get_rank(data)
        elif choice == "4":
            update_score(data)
        elif choice == "5":
            delete_one_record(data)
        elif choice == "6":
            calculate_average(data)
        elif choice == "7":
            filter_by_pass_fail(data)
        elif choice == "8":
            explicit_save(data)
        elif choice == "9":
            print("Exiting. Goodbye.")
            break
        elif choice == "10":
            set_max_score(data)
        else:
            print("Invalid choice. Enter a number from 1 to 10.")


if __name__ == "__main__":
    try:
        menu_loop()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
