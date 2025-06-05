#!/usr/bin/env python3
import argparse
import datetime
import time
import requests
from progressbar import progressbar

# ---------------------------
# Argument Parsing
# ---------------------------
parser = argparse.ArgumentParser(
    "grunt",
    description="A brute-force algorithm to potentially advance the Trench Crusade ARG.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

# Session crumb (cookie)
parser.add_argument(
    "-c", "--crumb",
    help="ID which is used to differentiate between valid sessions.",
    type=str
)

# File with potential passwords
parser.add_argument(
    "-t", "--test",
    help="File which contains potential passwords",
    type=str,
    default="test.txt",
    nargs='?'
)

# File to store tested passwords
parser.add_argument(
    "-td", "--tested",
    help="File to which store all tested passwords in.",
    type=str,
    default="tested.txt",
    nargs='?'
)

# Whether to generate passwords before testing
parser.add_argument(
    "-g", "--generate",
    help="Whether or not to generate passwords before testing.",
    default=False,
    action="store_true"
)

# Discord API token
parser.add_argument(
    "-d", "--discord",
    help="Discord authorization token.",
    type=str,
    nargs='?'
)

# Discord channel ID
parser.add_argument(
    "-ch", "--channel",
    help="Discord channel ID.",
    type=str,
    nargs='?'
)

# Discord message fetch limit
parser.add_argument(
    "-l", "--limit",
    help="Discord message limit.",
    type=int,
    default=100,
    nargs='?'
)

# First relevant Discord message ID
parser.add_argument(
    "-s", "--start",
    help="First relevant comment ID.",
    type=str,
    default="1374162399736762438",
    nargs='?'
)

args = parser.parse_args()

# ---------------------------
# Session Setup
# ---------------------------
s = requests.session()
# Initial GET to set up session cookies
s.get(
    "https://www.trenchcrusade.com/6d6574616d6f7270686973",
    headers={"DNT": "1", "Sec-GPC": "1", "Priority": "u=0, i"},
    cookies={"crumb": args.crumb}
)

# ---------------------------
# Constants
# ---------------------------
final_password = ""
testing_string = "===TESTING==="
done_string = "===DONE==="
generating_string = "===GENERATING==="

# Date after which to start fetching Discord messages
after_date = datetime.datetime(2025, 5, 20, tzinfo=datetime.timezone.utc)
after_timestamp = int(after_date.timestamp() * 1000)
after_snowflake = (after_timestamp - 1420070400000) << 22

# ---------------------------
# Fetch Discord Messages Until a Date
# ---------------------------
def get_messages_until_date(end_date):
    start_snowflake = args.start
    all_messages = []
    reached_end_date = False

    while not reached_end_date:
        # Prepare request parameters
        params = {'limit': args.limit, 'after': start_snowflake}

        # Make API request to Discord
        response = requests.get(
            f'https://discord.com/api/v10/channels/{args.channel}/messages',
            headers={'Authorization': args.discord},
            params=params
        )

        if not response.ok:
            raise Exception(f"API request failed: {response.status_code}")

        messages = response.json()
        if not messages:
            break

        # Process each message
        for message in messages:
            # Convert Discord timestamp to datetime
            message_timestamp = datetime.datetime.fromisoformat(message['timestamp'])

            # Stop if we've reached the end date
            if message_timestamp > end_date:
                reached_end_date = True
                break

            all_messages.append(message)

        # Update for next batch
        last_message_timestamp = messages[-1]['timestamp']
        start_snowflake = messages[-1]['id']

        # Progress feedback
        print(f'Fetched another {len(messages)} messages up to {last_message_timestamp}', end='\r')

        # Cache messages to file
        with open("temp.txt", "a", encoding="utf-8") as cache_file:
            cache_file.writelines(f"{msg['content']}\n" for msg in messages)

        # Respect Discord rate limits
        time.sleep(0.2)

    return all_messages

# ---------------------------
# Generate Passwords from Discord Messages
# ---------------------------
def generate() -> list[str]:
    end_date = datetime.datetime(2025, 5, 30, tzinfo=datetime.timezone.utc)
    messages = get_messages_until_date(end_date)
    print(messages)
    # Return non-empty message contents
    return [x['content'] for x in messages if x['content'].strip()]

# ---------------------------
# Test Passwords Against API
# ---------------------------
def test() -> str:
    testfile_content = []
    # Read potential passwords
    with open(args.test, "r", encoding="utf8") as test_file:
        testfile_content = test_file.read().splitlines()

    for i in progressbar(range(len(testfile_content))):
        line_entry = testfile_content[i]
        if line_entry.strip():
            # Skip if already tested
            with open(args.tested, "r", encoding="utf8") as tested_file:
                if line_entry.lower() in tested_file.read():
                    continue

            # Try lowercase
            r1 = s.post(
                "https://www.trenchcrusade.com/api/auth/visitor/collection",
                params={"crumb": args.crumb},
                json={"password": line_entry.lower(), "collectionId": "680897a38eba8b1b034f8e1d"},
                cookies={"crumb": args.crumb}
            )
            while r1.status_code == 429:  # Too many requests
                r1 = s.post(
                    "https://www.trenchcrusade.com/api/auth/visitor/collection",
                    params={"crumb": args.crumb},
                    json={"password": line_entry.lower(), "collectionId": "680897a38eba8b1b034f8e1d"},
                    cookies={"crumb": args.crumb}
                )

            # Try capitalized
            r2 = s.post(
                "https://www.trenchcrusade.com/api/auth/visitor/collection",
                params={"crumb": args.crumb},
                json={"password": line_entry.capitalize(), "collectionId": "680897a38eba8b1b034f8e1d"},
                cookies={"crumb": args.crumb}
            )
            while r2.status_code == 429:  # Too many requests
                r2 = s.post(
                    "https://www.trenchcrusade.com/api/auth/visitor/collection",
                    params={"crumb": args.crumb},
                    json={"password": line_entry.capitalize(), "collectionId": "680897a38eba8b1b034f8e1d"},
                    cookies={"crumb": args.crumb}
                )

            # Success if status code is 2xx
            if 200 <= r1.status_code < 300:
                return line_entry.lower()
            if 200 <= r2.status_code < 300:
                return line_entry.capitalize()

            # Mark as tested
            with open(args.tested, "a", encoding="utf8") as tested_file:
                tested_file.writelines(line_entry.lower() + '\n')
    return ""

# ---------------------------
# Print Final Result
# ---------------------------
def done() -> None:
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
        generated_passwords = generate()
        # Read existing passwords
        with open(args.test, "r", encoding="utf8") as test_file:
            saved_passwords = test_file.read().splitlines()
        # Merge and deduplicate
        unique_passwords = list(set(saved_passwords + generated_passwords))
        with open(args.test, "w", encoding="utf8") as test_file:
            test_file.write('\n'.join([x.strip() for x in unique_passwords if x.strip()]) + '\n')
        print(generating_string)

    print(testing_string)
    final_password = test()
    print(testing_string)

    print(done_string)
    done()
    print(done_string)
