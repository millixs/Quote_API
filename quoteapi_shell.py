import requests
import random
import time
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

API_BASE_URL = "https://zenquotes.io/api/"
MAX_RETRIES = 3


def exponential_backoff_delay(attempt):
    return 2 ** attempt  # 2, 4, 8 seconds


def get_user_choice():
    """
    Display menu and return the user's choice.
    """
    print("\n>> Initializing QuoteAPI Shell 2.0")
    print("[1] Random Quote")
    print("[2] Quote of the Day")
    print("[3] Keyword-based Quote")

    while True:
        try:
            choice = int(input("Choice > "))
            if choice == 0:
                print(">> Exiting QuoteAPI. Goodbye!")
                sys.exit()
            if choice in [1, 2, 3]:
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if choice == 1:
        return "random"
    elif choice == 2:
        return "today"
    else:
        keywords = input("Keyword/s > ")
        keywords = [kw.strip().lower() for kw in keywords.split(",")][:10]
        return f"keywords:{','.join(keywords)}"


def contains_keyword(text, keyword):
    words = text.lower().split()
    return keyword.lower() in words


def filter_quotes_by_keywords(quotes, keywords):
    matching_quotes = [
        q for q in quotes
        if any(contains_keyword(q.get('q', ''), k) for k in keywords) or
           any(contains_keyword(q.get('a', ''), k) for k in keywords)
    ]
    return matching_quotes


def fetch_quote(endpoint):
    """
    Fetch a quote from the API with retry mechanism and better error handling.
    """
    if "keywords:" in endpoint:
        keywords = endpoint.split(":")[1].split(",")
        print(f"\nSearching: {keywords}...")

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(f"{API_BASE_URL}quotes", timeout=10)
                if response.status_code == 200:
                    quotes = response.json()
                    matching_quotes = filter_quotes_by_keywords(quotes, keywords)

                    if matching_quotes:
                        return random.choice(matching_quotes)
                    else:
                        print(f"No quotes found containing the keywords {keywords}.")
                        for keyword in keywords:
                            fallback_quotes = filter_quotes_by_keywords(quotes, [keyword])
                            if fallback_quotes:
                                print(f"Found quotes for keyword '{keyword}':")
                                return random.choice(fallback_quotes)
                        return None
                else:
                    logging.warning(f"API error (status {response.status_code}).")
            except requests.exceptions.RequestException as e:
                logging.error(f"Network error: {str(e)}")

            delay = exponential_backoff_delay(attempt)
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

        print("Failed to fetch quotes after multiple attempts.")
        return None

    # For random and today quotes
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else None
            else:
                logging.warning(f"API error (status {response.status_code}).")
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {str(e)}")

        delay = exponential_backoff_delay(attempt)
        print(f"Retrying in {delay} seconds...")
        time.sleep(delay)

    print("Failed to fetch quote after multiple attempts.")
    return None


def main():
    """
    Main program that runs once and terminates.
    """
    choice = get_user_choice()
    quote_data = fetch_quote(choice)
    if quote_data:
        quote, author = quote_data['q'], quote_data['a']
        print(f'\n\033[93m"{quote}"\033[0m \n\t\033[96m~ {author}\033[0m \n')


if __name__ == "__main__":
    main()
