#!/usr/bin/env python3
"""
SAT Results Manager - Improved Version
Features:
1. Insert data
2. View all data (JSON)
3. Get rank
4. Update score
5. Delete one record
6. Calculate Average SAT Score
7. Filter records by Pass/Fail
8. Put the inserted data in json format in a file (explicit save)
9. Exit

Data is persisted to 'sat_data.json'. The script asks for a maximum SAT score on first run (default 1600).
Note: pass/fail is computed as score > 30% of the configured max score.

# hatchling - LLM generated code marker
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional


class SATResultsManager:
    """Main class for managing SAT results with improved structure and validation."""
    
    def __init__(self, data_file: str = "sat_data.json", default_max_score: int = 1600):
        self.data_file = data_file
        self.default_max_score = default_max_score
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file with proper error handling."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Validate data structure
                    if not isinstance(data, dict):
                        raise ValueError("Invalid data format")
                    if "max_score" not in data:
                        data["max_score"] = self.default_max_score
                    if "records" not in data:
                        data["records"] = {}
                    return data
            except (json.JSONDecodeError, ValueError, IOError) as e:
                print(f"Warning: Could not load data file ({e}). Starting with fresh data.")
                return {"max_score": self.default_max_score, "records": {}}
        else:
            return {"max_score": self.default_max_score, "records": {}}

    def save_data(self) -> bool:
        """Save data to JSON file with error handling."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"[Saved] Data written to {self.data_file}")
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    def validate_score(self, score_str: str) -> Optional[float]:
        """Validate and convert score input."""
        try:
            score = float(score_str.strip())
            if score < 0:
                print("Score cannot be negative.")
                return None
            if score > self.data["max_score"]:
                print(f"Score cannot exceed maximum ({self.data['max_score']}).")
                return None
            return score
        except ValueError:
            print("Please enter a valid numeric score.")
            return None

    def compute_pass(self, score: float) -> bool:
        """Calculate pass/fail status based on 30% threshold."""
        return score > 0.3 * self.data["max_score"]

    def validate_name(self, name: str) -> bool:
        """Validate candidate name."""
        name = name.strip()
        if not name:
            print("Name cannot be empty.")
            return False
        if len(name) > 100:
            print("Name too long (max 100 characters).")
            return False
        return True

    def insert_data(self) -> None:
        """Insert new candidate data with comprehensive validation."""
        print("\n" + "="*50)
        print("INSERT NEW CANDIDATE")
        print("="*50)
        
        # Get and validate name
        while True:
            name = input("Name (unique identifier): ").strip()
            if not self.validate_name(name):
                continue
            if name in self.data["records"]:
                print(f"Error: A record for '{name}' already exists.")
                return
            break

        # Get address information
        address = input("Address: ").strip()
        city = input("City: ").strip()
        country = input("Country: ").strip()
        
        # Validate pincode
        while True:
            pincode = input("Pincode: ").strip()
            if not pincode:
                print("Pincode cannot be empty.")
                continue
            if not pincode.isdigit() or len(pincode) < 3:
                print("Please enter a valid pincode (numbers only, min 3 digits).")
                continue
            break

        # Get and validate SAT score
        while True:
            score_input = input(f"SAT score (0-{self.data['max_score']}): ").strip()
            score = self.validate_score(score_input)
            if score is not None:
                break

        # Calculate pass status
        passed = self.compute_pass(score)

        # Create record
        record = {
            "name": name,
            "address": address,
            "city": city,
            "country": country,
            "pincode": pincode,
            "sat_score": score,
            "passed": passed,
        }

        # Save record
        self.data["records"][name] = record
        if self.save_data():
            print(f"\n✅ Successfully added {name} (Score: {score}, Status: {'PASS' if passed else 'FAIL'})")
        else:
            # Rollback if save failed
            del self.data["records"][name]
            print("❌ Failed to save data. Record not added.")

    def view_all_data(self) -> None:
        """Display all records in JSON format."""
        print("\n" + "="*50)
        print("ALL RECORDS (JSON FORMAT)")
        print("="*50)
        
        if not self.data["records"]:
            print("📝 No records available.")
            return
        
        display_data = {
            "max_score": self.data["max_score"],
            "total_candidates": len(self.data["records"]),
            "records": self.data["records"]
        }
        
        print(json.dumps(display_data, indent=2, ensure_ascii=False))

    def get_rank(self) -> None:
        """Get rank for a specific candidate."""
        print("\n" + "="*50)
        print("GET CANDIDATE RANK")
        print("="*50)
        
        if not self.data["records"]:
            print("📝 No records available for ranking.")
            return

        name = input("Enter candidate name: ").strip()
        if name not in self.data["records"]:
            print(f"❌ Candidate '{name}' not found.")
            self._suggest_similar_names(name)
            return

        candidate = self.data["records"][name]
        my_score = float(candidate["sat_score"])
        all_scores = [float(r["sat_score"]) for r in self.data["records"].values()]

        # Calculate rank (1-based, with ties handling)
        higher_count = sum(1 for score in all_scores if score > my_score)
        rank = higher_count + 1
        
        # Count candidates with same score
        same_score_count = sum(1 for score in all_scores if score == my_score)
        total_candidates = len(all_scores)
        
        # Calculate percentile
        percentile = ((total_candidates - rank + 1) / total_candidates) * 100

        print(f"\n🏆 RANKING RESULTS FOR {name.upper()}")
        print(f"   Score: {my_score}")
        print(f"   Rank: {rank} out of {total_candidates}")
        print(f"   Percentile: {percentile:.1f}%")
        print(f"   Status: {'✅ PASS' if candidate['passed'] else '❌ FAIL'}")
        
        if same_score_count > 1:
            print(f"   Note: {same_score_count} candidate(s) have the same score")

    def _suggest_similar_names(self, name: str) -> None:
        """Suggest similar names if exact match not found."""
        similar = [n for n in self.data["records"].keys() 
                  if name.lower() in n.lower() or n.lower() in name.lower()]
        if similar:
            print(f"💡 Did you mean: {', '.join(similar[:3])}")

    def update_score(self) -> None:
        """Update SAT score for an existing candidate."""
        print("\n" + "="*50)
        print("UPDATE CANDIDATE SCORE")
        print("="*50)
        
        if not self.data["records"]:
            print("📝 No records to update.")
            return

        name = input("Enter candidate name to update: ").strip()
        if name not in self.data["records"]:
            print(f"❌ Candidate '{name}' not found.")
            self._suggest_similar_names(name)
            return

        current_record = self.data["records"][name]
        print(f"Current score for {name}: {current_record['sat_score']}")

        while True:
            new_score_input = input(f"New SAT score (0-{self.data['max_score']}): ").strip()
            new_score = self.validate_score(new_score_input)
            if new_score is not None:
                break

        # Update record
        old_score = current_record['sat_score']
        old_status = current_record['passed']
        
        current_record["sat_score"] = new_score
        current_record["passed"] = self.compute_pass(new_score)
        
        if self.save_data():
            print(f"\n✅ Score updated for {name}:")
            print(f"   Old: {old_score} ({'PASS' if old_status else 'FAIL'})")
            print(f"   New: {new_score} ({'PASS' if current_record['passed'] else 'FAIL'})")
        else:
            # Rollback if save failed
            current_record["sat_score"] = old_score
            current_record["passed"] = old_status
            print("❌ Failed to save updated score.")

    def delete_one_record(self) -> None:
        """Delete a single candidate record."""
        print("\n" + "="*50)
        print("DELETE CANDIDATE RECORD")
        print("="*50)
        
        if not self.data["records"]:
            print("📝 No records to delete.")
            return

        name = input("Enter candidate name to delete: ").strip()
        if name not in self.data["records"]:
            print(f"❌ Candidate '{name}' not found.")
            self._suggest_similar_names(name)
            return

        # Show record details before deletion
        record = self.data["records"][name]
        print(f"\n📋 Record to delete:")
        print(f"   Name: {record['name']}")
        print(f"   Score: {record['sat_score']}")
        print(f"   Status: {'PASS' if record['passed'] else 'FAIL'}")
        
        # Confirmation with exact match required
        confirm = input(f"\nType 'DELETE {name}' to confirm deletion: ").strip()
        if confirm == f"DELETE {name}":
            backup_record = self.data["records"][name].copy()
            del self.data["records"][name]
            
            if self.save_data():
                print(f"✅ Record for '{name}' has been deleted.")
            else:
                # Restore record if save failed
                self.data["records"][name] = backup_record
                print("❌ Failed to save changes. Record not deleted.")
        else:
            print("❌ Deletion cancelled. Exact confirmation required.")

    def calculate_average(self) -> None:
        """Calculate and display average SAT score."""
        print("\n" + "="*50)
        print("AVERAGE SAT SCORE ANALYSIS")
        print("="*50)
        
        if not self.data["records"]:
            print("📝 No records available for calculation.")
            return

        scores = [float(r["sat_score"]) for r in self.data["records"].values()]
        passed_scores = [s for s, r in zip(scores, self.data["records"].values()) if r["passed"]]
        failed_scores = [s for s, r in zip(scores, self.data["records"].values()) if not r["passed"]]

        avg_overall = sum(scores) / len(scores)
        pass_rate = (len(passed_scores) / len(scores)) * 100

        print(f"📊 STATISTICS ({len(scores)} candidates)")
        print(f"   Overall Average: {avg_overall:.2f} / {self.data['max_score']} ({avg_overall/self.data['max_score']*100:.1f}%)")
        print(f"   Pass Rate: {pass_rate:.1f}% ({len(passed_scores)} passed, {len(failed_scores)} failed)")
        print(f"   Passing Threshold: {0.3 * self.data['max_score']:.1f}")
        
        if passed_scores:
            avg_passed = sum(passed_scores) / len(passed_scores)
            print(f"   Average (Passed): {avg_passed:.2f}")
        
        if failed_scores:
            avg_failed = sum(failed_scores) / len(failed_scores)
            print(f"   Average (Failed): {avg_failed:.2f}")

    def filter_by_pass_fail(self) -> None:
        """Filter and display records by pass/fail status."""
        print("\n" + "="*50)
        print("FILTER BY PASS/FAIL STATUS")
        print("="*50)
        
        if not self.data["records"]:
            print("📝 No records available.")
            return

        choice = input("Enter 'pass' to show passed, 'fail' to show failed: ").strip().lower()
        if choice not in ("pass", "fail"):
            print("❌ Invalid choice. Please enter 'pass' or 'fail'.")
            return

        want_pass = choice == "pass"
        filtered_records = [r for r in self.data["records"].values() if r.get("passed") == want_pass]

        if not filtered_records:
            print(f"📝 No candidates with {choice.upper()} status found.")
            return

        print(f"\n{'✅ PASSED' if want_pass else '❌ FAILED'} CANDIDATES ({len(filtered_records)} found)")
        print("="*50)
        print(json.dumps(filtered_records, indent=2, ensure_ascii=False))

    def explicit_save(self) -> None:
        """Explicitly save data to JSON file."""
        print("\n" + "="*50)
        print("SAVE DATA TO JSON FILE")
        print("="*50)
        
        if self.save_data():
            print(f"✅ Data successfully saved to {self.data_file}")
            print(f"   Records: {len(self.data['records'])}")
            print(f"   Max Score: {self.data['max_score']}")
        else:
            print("❌ Failed to save data to file.")

    def set_max_score(self) -> None:
        """Set maximum SAT score and recalculate pass/fail status."""
        print(f"\n" + "="*50)
        print("SET MAXIMUM SAT SCORE")
        print("="*50)
        print(f"Current max score: {self.data['max_score']}")
        
        while True:
            new_max_input = input("Enter new maximum SAT score (or press Enter to cancel): ").strip()
            if new_max_input == "":
                print("❌ Operation cancelled.")
                return
            
            try:
                new_max = float(new_max_input)
                if new_max <= 0:
                    print("❌ Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number.")

        old_max = self.data["max_score"]
        self.data["max_score"] = new_max
        
        # Recalculate pass/fail for all records
        updated_count = 0
        for record in self.data["records"].values():
            old_status = record["passed"]
            record["passed"] = self.compute_pass(record["sat_score"])
            if old_status != record["passed"]:
                updated_count += 1

        if self.save_data():
            print(f"✅ Max score updated: {old_max} → {new_max}")
            if updated_count > 0:
                print(f"   {updated_count} candidate(s) had their pass/fail status updated.")
        else:
            # Rollback on save failure
            self.data["max_score"] = old_max
            for record in self.data["records"].values():
                record["passed"] = self.compute_pass(record["sat_score"])
            print("❌ Failed to save changes. Max score not updated.")

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*60)
        print("🎓 SAT RESULTS MANAGER")
        print("="*60)
        print("1.  Insert data")
        print("2.  View all data")
        print("3.  Get rank")
        print("4.  Update score")
        print("5.  Delete one record")
        print("6.  Calculate Average SAT Score")
        print("7.  Filter records by Pass/Fail Status")
        print("8.  Save data to JSON file")
        print("9.  Exit")
        print("10. Set maximum SAT score")
        print("-" * 60)
        print(f"📈 Current Stats: {len(self.data['records'])} candidates, Max Score: {self.data['max_score']}")

    def run(self) -> None:
        """Main program loop."""
        # Welcome message
        if not self.data["records"] and self.data["max_score"] == self.default_max_score:
            print("🎓 Welcome to SAT Results Manager!")
            print(f"Default max score is {self.default_max_score}. You can change this in the menu.")

        while True:
            try:
                self.display_menu()
                choice = input("\nChoose an option (1-10): ").strip()
                
                if choice == "1":
                    self.insert_data()
                elif choice == "2":
                    self.view_all_data()
                elif choice == "3":
                    self.get_rank()
                elif choice == "4":
                    self.update_score()
                elif choice == "5":
                    self.delete_one_record()
                elif choice == "6":
                    self.calculate_average()
                elif choice == "7":
                    self.filter_by_pass_fail()
                elif choice == "8":
                    self.explicit_save()
                elif choice == "9":
                    print("\n👋 Thank you for using SAT Results Manager. Goodbye!")
                    break
                elif choice == "10":
                    self.set_max_score()
                else:
                    print("❌ Invalid choice. Please enter a number from 1 to 10.")
                
                # Pause before showing menu again
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Program interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")
                print("Please try again or contact support if the problem persists.")


def main():
    """Entry point of the application."""
    try:
        manager = SATResultsManager()
        manager.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()