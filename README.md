# grunt

A brute-force tool for password guessing in the [Trench Crusade ARG](https://www.trenchcrusade.com/6d6574616d6f7270686973).

---

## Features

- Brute-force password attempts using a wordlist
- Optionally generate password candidates from Discord channel messages
- Tracks tested passwords to avoid duplicates
- Supports Discord API integration for message scraping

---

## Installation

```sh
pip install -r requirements.txt
```

---

## Usage

Display help and all options:

```sh
python grunt.py --help
```

### Basic Example

Brute-force using a wordlist:

```sh
python grunt.py -c YOUR_CRUMB
```

### With Password Generation from Discord

Generate passwords from Discord messages before testing:

```sh
python grunt.py -g -c YOUR_CRUMB -d YOUR_DISCORD_TOKEN -ch YOUR_CHANNEL_ID
```

---

## Arguments

| Argument         | Description                                      | Required | Default         |
|------------------|--------------------------------------------------|----------|-----------------|
| `-c, --crumb`    | Session crumb (cookie) for authentication        | Yes      | —               |
| `-t, --test`     | File with potential passwords                    | No       | `test.txt`      |
| `-td, --tested`  | File to store all tested passwords               | No       | `tested.txt`    |
| `-g, --generate` | Generate passwords from Discord messages         | No       | `False`         |
| `-d, --discord`  | Discord API token                                | If `-g`  | —               |
| `-ch, --channel` | Discord channel ID                               | If `-g`  | —               |
| `-l, --limit`    | Discord message fetch limit                      | No       | `100`           |
| `-s, --start`    | First relevant Discord message ID                | No       | (preset value)  |

---

## How to Find Your Crumb

The crumb is a session cookie required for authentication.  
You can find it in your browser's developer tools after logging in to the Trench Crusade website.

![Crumb Example](/assets/crumb.png)

---

## Notes

- Use responsibly and respect rate limits.
- For Discord scraping, your token must have access to the specified channel.
- Tested passwords are logged to avoid redundant attempts.

---

## License

MIT License