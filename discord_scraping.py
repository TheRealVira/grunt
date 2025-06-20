import datetime
import time
import requests

def get_messages_until_date(args, end_date):
    """
    Fetches Discord messages from a channel until a specified end date.
    Returns a list of message objects.
    """
    start_snowflake = args.start
    all_messages = []
    reached_end_date = False
    seen_ids = set()

    while not reached_end_date:
        params = {'limit': args.limit, 'after': start_snowflake}
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

        # Filter out already seen messages (prevents infinite loop)
        new_messages = [m for m in messages if m['id'] not in seen_ids]
        if not new_messages:
            break  # No new messages, stop looping

        for message in new_messages:
            seen_ids.add(message['id'])
            message_timestamp = datetime.datetime.fromisoformat(message['timestamp'])
            if message_timestamp > end_date:
                reached_end_date = True
                break
            all_messages.append(message)

        # Update for next batch
        last_message_id = new_messages[-1]['id']
        start_snowflake = last_message_id

        with open("temp.txt", "a", encoding="utf-8") as cache_file:
            cache_file.writelines(f"{msg['content']}\n" for msg in new_messages)

        time.sleep(0.2)

    return all_messages

def generate_passwords_from_discord(args, end_date):
    """
    Generates a list of password candidates from Discord messages.
    """
    messages = get_messages_until_date(args, end_date)
    return [x['content'] for x in messages if x['content'].strip()]