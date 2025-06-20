#!/usr/bin/env python3
import argparse
import datetime
import requests

from discord_scraping import generate_passwords_from_discord
from bruteforce import test_passwords

# ---------------------------
# Argument Parsing
# ---------------------------
parser = argparse.ArgumentParser(
    "grunt",
    description="A brute-force algorithm to potentially advance the Trench Crusade ARG.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-c", "--crumb",
    help="ID which is used to differentiate between valid sessions.",
    type=str,
    required=True
)
parser.add_argument(
    "-t", "--test",
    help="File which contains potential passwords",
    type=str,
    default="test.txt"
)
parser.add_argument(
    "-td", "--tested",
    help="File to which store all tested passwords in.",
    type=str,
    default="tested.txt"
)
parser.add_argument(
    "-g", "--generate",
    help="Whether or not to generate passwords before testing.",
    default=False,
    action="store_true"
)
parser.add_argument(
    "-d", "--discord",
    help="Discord authorization token.",
    type=str
)
parser.add_argument(
    "-ch", "--channel",
    help="Discord channel ID.",
    type=str
)
parser.add_argument(
    "-l", "--limit",
    help="Discord message limit.",
    type=int,
    default=100
)
parser.add_argument(
    "-s", "--start",
    help="First relevant comment ID.",
    type=str,
    default="1374162399736762438"
)
parser.add_argument(
    "-cid", "--collection-id",
    help="Collection ID to brute-force against.",
    type=str,
    default="680897a38eba8b1b034f8e1d"
)

args = parser.parse_args()

# ---------------------------
# Session Setup
# ---------------------------
s = requests.session()
s.get(
    "https://www.trenchcrusade.com/" + args.collection_id,
    headers={"DNT": "1", "Sec-GPC": "1", "Priority": "u=0, i"},
    cookies={"crumb": args.crumb}
)

# ---------------------------
# Constants
# ---------------------------
testing_string = "===TESTING==="
done_string = "===DONE==="
generating_string = "===GENERATING==="

# ---------------------------
# Print Final Result
# ---------------------------
def done(final_password) -> None:
    if final_password:
        print("Password was found: '" + final_password + "'")
    else:
        print("No valid password was found.")

# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    if args.generate:
        print(generating_string)
        end_date = datetime.datetime(2025, 5, 30, tzinfo=datetime.timezone.utc)
        generated_passwords = generate_passwords_from_discord(args, end_date)
        # Read existing passwords
        with open(args.test, "r", encoding="utf8") as test_file:
            saved_passwords = test_file.read().splitlines()
        # Merge and deduplicate
        unique_passwords = list(set(saved_passwords + generated_passwords))
        with open(args.test, "w", encoding="utf8") as test_file:
            test_file.write('\n'.join([x.strip() for x in unique_passwords if x.strip()]) + '\n')
        print(generating_string)

    print(testing_string)
    final_password = test_passwords(args, s)
    print(testing_string)

    print(done_string)
    done(final_password)
    print(done_string)
