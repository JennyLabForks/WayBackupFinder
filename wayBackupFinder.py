import os
import requests
import time
import logging

from threading import Thread
from itertools import cycle


logger = logging.getLogger(__name__)

MAX_TRIES = 3  # Maximum number of retries
RETRY_DELAY = 5  # Delay between retries (in seconds)
ATTEMPT = 0
MAX_TIMEOUT=60
TOTAL_LINES = 1000

class WayBackupFinder:
    def __init__(self,domain_path,file_path='extension.txt'):
        self.domain = domain
        self.file_path = file_path
        self.domains = []
        self.snapshot_urls = []

    
    # Load extensions from file
    def load_extensions_from_file(self):
        try:
            with open(self.file_path, 'r') as f:
                extensions = [line.strip() for line in f.readlines() if line.strip()]
            return extensions
        except FileNotFoundError:
            logger.error(f"[ERROR] WayBackupFinder::load_extensions_from_file(): {file_path} not found. Proceeding with no extensions.")
            return []
    
    # Load domains from file
    def load_domains_from_file(self):
        try:
            with open(self.file_path, 'r') as f:
                self.domains = [line.strip() for line in f.readlines() if line.strip()]
            return self.domains
        except FileNotFoundError:
            logger.error(f"[ERROR] WayBackupFinder::load_domains_from_file(): {file_path} not found. Exiting.")
            return
    
    # Fetch URLs using The Wayback Machine API with streaming and backoff
    def fetch_urls(target, file_extensions):
        logger.info(f"[INFO] WayBackupFinder::load_domains_from_file(): Fetching URLs from The Time Machine Lite for {target}... "
        print(f"\n")
        archive_url = f'https://web.archive.org/cdx/search/cdx?url=*.{target}/*&output=txt&fl=original&collapse=urlkey&page=/'
    
        global stop_loader
        stop_loader = False
        loader_thread = Thread(target=loader_animation, args=("Fetching URLs...",))
        loader_thread.start()
    
  
    
        while ATTEMPT < MAX_RETRIES:
            try:
                with requests.get(archive_url, stream=True, timeout=MAX_TIMEOUT) as response:  # Stream the response
                    response.raise_for_status()
                    loggeer.info("[IINFO] Streaming response from archive...")
    
                    url_list = []
                    ltotal_lines = 0
                    for line in response.iter_lines(decode_unicode=True):  # Process each line incrementally
                        if line:
                            url_list.append(line)
                            ltotal_lines += 1
                            if ltotal_lines % TOTAL_LINES == 0:  # Show progress every 1000 lines
                                logger.info(f"[INFO] Fetched {ltotal_lines} URLs...", end="")
    
                    logginger.info(f"[INFO] Fetched {TOTAL_LINES} URLs from archive."))
                    stop_loader = True
                    loader_thread.join()
                    return {ext: [url for url in url_list if url.lower().endswith(ext.lower())] for ext in file_extensions}
            except requests.exceptions.RequestException as e:
                attempt += 1
                if attempt < max_retries:
                    logger.warning(f"[WARN] Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"[ERROR] Error fetching URLs after {max_retries} attempts: {e}")
                    time.sleep(300)  # Sleep for 5 minutes (300 seconds)
                    return {}  # Return an empty dictionary after backoff
    
    # Check for archived snapshots
    def check_wayback_snapshot(url):
        wayback_url = f'https://archive.org/wayback/available?url={url}'
        try:
            response = requests.get(wayback_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
                snapshot_url = data["archived_snapshots"]["closest"].get("url")
                if snapshot_url:
                    print(f"[+] Found possible backup: {colored(snapshot_url, 'green')}")
                    self.snapshot_urls.append(snapshot_url)
            else:
                print(f"[-] No archived snapshot found for {url}.")
        except Exception as e:
            print(f"[?] Error checking Wayback snapshot for {url}: {e}")
    
    # Save filtered URLs
    def save_urls(target, extension_stats, file_suffix="_filtered_urls.txt"):
        folder = f"content/{target}"
        os.makedirs(folder, exist_ok=True)
        all_filtered_urls = []
        for ext, urls in extension_stats.items():
            if urls:
                file_path = os.path.join(folder, f"{target}_{ext.strip('.')}"+file_suffix)
                with open(file_path, 'w') as file:
                    file.write("\n".join(urls))
                all_filtered_urls.extend(urls)
                print(f"Filtered URLs for {ext} saved to: {colored(file_path, 'green')}")
        return all_filtered_urls
    
    # Process domain
    def process_domain(target, file_extensions):
        extension_stats = fetch_urls(target, file_extensions)
        if not extension_stats:  # Ensure extension_stats is not empty
            print(colored(f"No URLs fetched for {target}. Skipping...", "yellow"))
            return
        all_filtered_urls = save_urls(target, extension_stats)
        for url in all_filtered_urls:
            check_wayback_snapshot(url)

# Main execution
if __name__ == "__main__":


    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} <domain_list_input.txt>")

    filepath = sys.argv[1]
    WayBackupFinder()    
    domains = load_domains_from_file(domain_file)
    
    # Load default extensions from file
    default_extensions = load_extensions_from_file()
    choice = input("Use custom file extensions or load from extensions.txt? (custom/load): ").strip().lower()
    elif choice == "load" and default_extensions:
        file_extensions = default_extensions
    # Process each domain
    for target in domains:
        process_domain(target, file_extensions)

    print(colored("\nProcess complete for all domains.", "green"))
