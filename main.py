import httpx
from bs4 import BeautifulSoup
import time
import random
import os
import requests

# Load Ethereum addresses from file
def load_addresses_from_file(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]
# Telegram bot settings
BOT_TOKEN = '7997927855:AAGhQHFhmULHhr-cZV7K4lcGBTaDiFugqws'
CHAT_ID = '759264436'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Realistic User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97",
    "Mozilla/5.0 (X11; CrOS x86_64 14588.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.23.211.8 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 YaBrowser/24.3.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 OPR/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Vivaldi/6.5.3266.69 Safari/537.36"
]

# Function to scrape number of addresses from Blockchair
def get_number_of_addresses(address, client):
    url = f"https://blockchair.com/search?q={address}"
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.5"
    }

    try:
        response = client.get(url, headers=headers)
        if response.status_code == 429:
            print("⚠️ Rate limit hit! Sleeping for 10 seconds...")
            time.sleep(10)
            return None

        if response.status_code != 200:
            print(f"🚫 Status code {response.status_code} for {address}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <h2> tag containing "Addresses • X" 
        h2_tag = soup.find('h2', class_='fs-md fw-semibold')
        if h2_tag:
            text = h2_tag.get_text(strip=True)
            parts = text.split('•')
            if len(parts) == 2:
                num_addresses = parts[1].strip()
                if num_addresses.isdigit():
                    num_addresses = int(num_addresses)
                    if num_addresses > 0:
                        result = f"{address} | Number of Addresses: {num_addresses}"
                        print(result)
                        send_telegram_message(result)
                        return result

        # If no valid number of addresses found
        return None

    except Exception as e:
        print(f"❌ Error fetching {address}: {str(e)}")
        print("⚠️ So! Sleeping for 10 seconds...")
        time.sleep(10)
        return None


def main():
    results = []

    addresses = load_addresses_from_file(r"ooo.txt")

    with httpx.Client(timeout=30) as client:
        for address in addresses:
            balance_result = get_number_of_addresses(address, client)
            if balance_result:
                results.append(balance_result)

            # Fixed delay between requests
            delay = random.uniform(0.0001, 0.0002)
            time.sleep(delay)

    

    print("\n✅ All Done. ")


if __name__ == "__main__":
    main()
