# wolper-google

Command-line tool to read data from Google Calendar and Gmail using an OAuth access token.

## Requirements

- Python 3.11+
- `uv`

## Install

```bash
uv sync
```

## Auth file

By default the CLI reads `~/.googleauth.json` with the following shape:

```json
{
  "access_token": "...",
  "expires_at": "2026-02-20T16:55:09.859080+00:00",
  "token_type": "Bearer"
}
```

You can pass a different file with `--auth-file`.

## Quick start

```bash
# calendar list (formatted)
uv run wolper-google --auth-file ./testauth.json calendar list

# gmail list (formatted)
uv run wolper-google --auth-file ./testauth.json gmail list

# raw JSON output
uv run wolper-google --auth-file ./testauth.json calendar list --raw
uv run wolper-google --auth-file ./testauth.json gmail list --raw
```

## Output format

- Default output is formatted as `id<TAB>name` for the two list commands:
  - `calendar list` prints `calendarId` and `summary`
  - `gmail list` prints `labelId` and `name`
- All other commands print raw JSON.
- `--raw` forces raw JSON output even for the formatted list commands.

## Calendar commands

```bash
# calendar list
uv run wolper-google --auth-file ./testauth.json calendar list

# calendar metadata
uv run wolper-google --auth-file ./testauth.json calendar get --calendar-id markus@wolpertec.com

# calendar list entries
uv run wolper-google --auth-file ./testauth.json calendar calendarlist list
uv run wolper-google --auth-file ./testauth.json calendar calendarlist get --calendar-id markus@wolpertec.com

# ACLs
uv run wolper-google --auth-file ./testauth.json calendar acl list --calendar-id markus@wolpertec.com
uv run wolper-google --auth-file ./testauth.json calendar acl get --calendar-id markus@wolpertec.com --rule-id <RULE_ID>

# events
uv run wolper-google --auth-file ./testauth.json calendar events list --calendar-id markus@wolpertec.com
uv run wolper-google --auth-file ./testauth.json calendar events get --calendar-id markus@wolpertec.com --event-id <EVENT_ID>
uv run wolper-google --auth-file ./testauth.json calendar events instances --calendar-id markus@wolpertec.com --event-id <EVENT_ID>

# colors
uv run wolper-google --auth-file ./testauth.json calendar colors get

# settings
uv run wolper-google --auth-file ./testauth.json calendar settings list
uv run wolper-google --auth-file ./testauth.json calendar settings get --setting locale
```

### Calendar query params

Use `--param key=value` on list/get commands that accept query parameters.

```bash
# list events between dates (RFC3339)
uv run wolper-google --auth-file ./testauth.json calendar events list \
  --calendar-id markus@wolpertec.com \
  --param timeMin=2026-02-01T00:00:00Z \
  --param timeMax=2026-03-01T00:00:00Z

# limit results
uv run wolper-google --auth-file ./testauth.json calendar events list \
  --calendar-id markus@wolpertec.com \
  --param maxResults=5
```

## Gmail commands

```bash
# label list (formatted)
uv run wolper-google --auth-file ./testauth.json gmail list

# label list (raw JSON)
uv run wolper-google --auth-file ./testauth.json gmail labels list

# label metadata
uv run wolper-google --auth-file ./testauth.json gmail labels get --label-id INBOX

# drafts
uv run wolper-google --auth-file ./testauth.json gmail drafts list
uv run wolper-google --auth-file ./testauth.json gmail drafts get --draft-id <DRAFT_ID>

# history (requires start history id)
uv run wolper-google --auth-file ./testauth.json gmail history list --start-history-id <HISTORY_ID>

# messages
uv run wolper-google --auth-file ./testauth.json gmail messages list
uv run wolper-google --auth-file ./testauth.json gmail messages get --message-id <MESSAGE_ID>

# attachments
uv run wolper-google --auth-file ./testauth.json gmail attachments get --message-id <MESSAGE_ID> --attachment-id <ATTACHMENT_ID>

# profile
uv run wolper-google --auth-file ./testauth.json gmail profile get

# settings
uv run wolper-google --auth-file ./testauth.json gmail settings auto-forwarding get
uv run wolper-google --auth-file ./testauth.json gmail settings filters list
uv run wolper-google --auth-file ./testauth.json gmail settings filters get --filter-id <FILTER_ID>
uv run wolper-google --auth-file ./testauth.json gmail settings forwarding-addresses list
uv run wolper-google --auth-file ./testauth.json gmail settings forwarding-addresses get --forwarding-email user@example.com
uv run wolper-google --auth-file ./testauth.json gmail settings imap get
uv run wolper-google --auth-file ./testauth.json gmail settings pop get
uv run wolper-google --auth-file ./testauth.json gmail settings send-as list
uv run wolper-google --auth-file ./testauth.json gmail settings send-as get --send-as-email me@example.com
uv run wolper-google --auth-file ./testauth.json gmail settings smime list --send-as-email me@example.com
uv run wolper-google --auth-file ./testauth.json gmail settings smime get --send-as-email me@example.com --smime-id <SMIME_ID>
uv run wolper-google --auth-file ./testauth.json gmail settings vacation get

# threads
uv run wolper-google --auth-file ./testauth.json gmail threads list
uv run wolper-google --auth-file ./testauth.json gmail threads get --thread-id <THREAD_ID>
```

### Gmail query params

Use `--param key=value` on list/get commands that accept query parameters.

```bash
# search messages
uv run wolper-google --auth-file ./testauth.json gmail messages list \
  --param q="from:someone@example.com subject:invoice"

# limit results
uv run wolper-google --auth-file ./testauth.json gmail messages list \
  --param maxResults=5

# request full message payload
uv run wolper-google --auth-file ./testauth.json gmail messages get \
  --message-id <MESSAGE_ID> \
  --param format=full
```

## Notes

- `calendar list` and `gmail list` are convenience commands that map to the Calendar list and Gmail labels list endpoints.
- For anything else, use the structured subcommands under `calendar` and `gmail`.
