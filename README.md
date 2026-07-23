# QuoteAPI Shell

A command-line quote fetcher built in Python that retrieves random quotes, the quote of the day, or quotes matching user-specified keywords, using the [ZenQuotes API](https://zenquotes.io/). The tool includes retry logic with exponential backoff to handle transient network or API failures gracefully.

## Overview

QuoteAPI Shell is a lightweight, interactive command-line application for exploring quotes without leaving the terminal. It was built to demonstrate practical handling of external API calls, including error handling, retries, and basic text filtering, wrapped in a simple text-based menu interface.

## Features

- **Random Quote** — Fetches a random quote from the ZenQuotes API.
- **Quote of the Day** — Retrieves the daily featured quote.
- **Keyword-Based Search** — Searches quote text and author names for one or more comma-separated keywords (up to 10) and returns a matching quote at random.
- **Fallback Matching** — If no quote matches all provided keywords, the tool automatically retries with each keyword individually before giving up.
- **Retry with Exponential Backoff** — Automatically retries failed API requests up to 3 times, with increasing delay (2s, 4s, 8s) between attempts.
- **Structured Logging** — Uses Python's `logging` module to report warnings and errors during API calls.
- **Colored Terminal Output** — Displays the returned quote and author using ANSI color codes for readability.

## How It Works

1. The user is presented with a menu and selects one of three modes: random quote, quote of the day, or keyword search.
2. For random and daily quotes, the app sends a single request to the corresponding ZenQuotes endpoint.
3. For keyword search, the app retrieves the full list of available quotes, then filters them locally by checking whether any of the supplied keywords appear as whole words in the quote text.
4. If a request fails due to a network error or a non-200 response, the app waits using an exponential backoff delay and retries, up to a maximum of 3 attempts.
5. If no exact keyword match is found across all keywords combined, the app falls back to searching for each keyword individually before returning no result.
6. The final quote and author are printed to the terminal in color.

## Requirements

- Python 3.7 or higher
- [requests](https://pypi.org/project/requests/) library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/millixs/Quote_API.git
   cd Quote_API
   ```

2. Install the required dependency:
   ```bash
   pip install requests
   ```

## Usage

Run the script from the terminal:

```bash
python quoteapi_shell.py
```

You will be presented with a menu:

```
>> Initializing QuoteAPI Shell 2.0
[1] Random Quote
[2] Quote of the Day
[3] Keyword-based Quote
Choice >
```

- Enter `1` for a random quote.
- Enter `2` for the quote of the day.
- Enter `3` to search by keyword(s), then enter one or more comma-separated keywords when prompted.
- Enter `0` at any time to exit the program.

## Outputs

**Option 1 — Random Quote**

![Random Quote output](Screenshots/img1.png)

Selecting option 1 fetches a completely random quote from the ZenQuotes API and prints it to the terminal along with its author. No additional input is required beyond the initial menu choice.

**Option 2 — Quote of the Day**

![Quote of the Day output](Screenshots/img2.png)

Selecting option 2 retrieves the ZenQuotes "quote of the day" — a single featured quote that stays the same for all users until it refreshes the next day.

**Option 3 — Keyword-based Quote**

![Keyword-based Quote output](Screenshots/img3.png)

Selecting option 3 prompts the user to enter up to 10 comma-separated keywords. The app then searches the full list of available quotes and returns one at random whose text contains at least one of the given keywords. If no single quote matches all the keywords together, the app automatically falls back to searching keyword by keyword until a match is found.

## Error Handling

The application is designed to fail gracefully:

- Invalid menu input is caught and re-prompted without crashing the program.
- Network errors (timeouts, connection issues) are logged and trigger an automatic retry.
- Non-200 API responses are logged as warnings and also trigger a retry.
- After all retry attempts are exhausted, the program informs the user and exits the current operation cleanly rather than throwing an unhandled exception.

## Project Structure

```
quoteapi-shell/
├── Screenshots/         # Example screenshots of the application in use
├── quoteapi_shell.py    # Main application script
└── README.md
```

## Potential Improvements

- Add unit tests for keyword filtering and retry logic.
- Support caching of quotes to reduce redundant API calls.
- Add command-line arguments for non-interactive usage.
- Support exporting fetched quotes to a file (e.g., JSON or CSV).

## License

This project is available under the MIT License. See the LICENSE file for details.


