import requests
import argparse
import random
import time
import threading
import sys
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
]

visited_urls = set()
lock = threading.Lock()

def fetch_directory(url, wordlist, filter_errors, delay, threads):
    with open(wordlist, 'r') as file:
        directories = [line.strip() for line in file]
    
    def fetch_dir(directory):
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        target_url = urljoin(url, directory)

        with lock:
            if target_url in visited_urls:
                return
            visited_urls.add(target_url)

        try:
            response = requests.get(target_url, headers=headers, timeout=10)
            status_code = response.status_code
            
            if status_code == 200:
                print(f"Found: {target_url}")
            elif filter_errors and status_code in [403, 404, 429]:
                pass
            else:
                print(f"Checked: {target_url} - {status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to {target_url}: {str(e)}")
        
        if delay > 0:
            time.sleep(delay)

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_directory = {executor.submit(fetch_dir, directory): directory for directory in directories}
            
            for future in as_completed(future_to_directory):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error occurred: {str(e)}")

    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Shutting down...")
        executor.shutdown(wait=False)
        raise
    finally:
        sys.stderr.write("\nMade by corndog16\n")

def main():
    parser = argparse.ArgumentParser(description='A fast, multithreaded web directory crawler.')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file for directories')
    parser.add_argument('-f', '--filter', action='store_true', help='Filter out 403, 404, and 429 errors')
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay between requests in seconds')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads to use')

    args = parser.parse_args()

    fetch_directory(args.url, args.wordlist, args.filter, args.delay, args.threads)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess terminated by user. Exiting...")
