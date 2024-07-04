#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import hashlib
import random
import signal
import sys
from threading import Thread, Lock, current_thread
from queue import Queue
from datetime import datetime
import pandas as pd
import os
from urllib.parse import urljoin, urlparse
import time

# Initialize a set to store crawled URLs and a lock for thread-safe operations
crawled_urls = set()
crawled_urls_lock = Lock()

# Initialize a dictionary to store visited URLs and their hash values
visited_urls = {}
visited_urls_lock = Lock()

# Initialize a queue for URLs to be crawled
url_queue = Queue()

# Initialize a DataFrame to store visited URLs and their hash values
data_frame_1 = pd.DataFrame(columns=['url', 'hash'])

# List of User-Agents to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1'
]

# SQLite database file path
sqlite_db_file = 'urls.db'

# Function to initialize SQLite database and tables
def init_sqlite_db():
    """Initialize SQLite database and necessary tables."""
    conn = sqlite3.connect(sqlite_db_file)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawled_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            UNIQUE(url)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visited_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            hash TEXT NOT NULL,
            UNIQUE(url)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize SQLite database
init_sqlite_db()

# Function to fetch page content
def fetch_page(session, url):
    """Fetch the content of the page at the given URL."""
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200 and response.text.strip():  # Check for non-empty content
            return response.text
        else:
            print(f"Non-200 status code or empty content {response.status_code} for {url}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract links from HTML content
def get_links(html_content, base_url):
    """Extract and return all the links from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return links

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print('Interrupted! Saving checkpoint and visited URLs to CSV...')
    save_checkpoint()
    save_visited_urls_csv()
    save_to_sqlite()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function to load the existing state from SQLite database
def load_from_sqlite():
    """Load the existing state of visited URLs from SQLite database."""
    global visited_urls
    try:
        conn = sqlite3.connect(sqlite_db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT url, hash FROM visited_urls')
        rows = cursor.fetchall()
        for row in rows:
            visited_urls[row[0]] = row[1]
        conn.close()
        print("Loaded visited URLs from SQLite database.")
    except Exception as e:
        print(f"Error loading from SQLite database: {e}")

# Function to save visited URLs to SQLite database
def save_to_sqlite():
    """Save visited URLs to SQLite database."""
    try:
        conn = sqlite3.connect(sqlite_db_file)
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute('DELETE FROM visited_urls')
        # Insert new data
        for url, hash_value in visited_urls.items():
            cursor.execute('INSERT INTO visited_urls (url, hash) VALUES (?, ?)', (url, hash_value))
        conn.commit()
        conn.close()
        print("Visited URLs saved to SQLite database.")
    except Exception as e:
        print(f"Error saving to SQLite database: {e}")

# Function to save the current state to a checkpoint file
def save_checkpoint():
    """Save the current state of visited URLs to a checkpoint file (master.csv)."""
    global data_frame_1
    with visited_urls_lock:
        all_urls_df = pd.read_csv('master.csv') if os.path.exists('master.csv') else pd.DataFrame(columns=['url', 'hash'])
        new_data_df = pd.DataFrame(list(visited_urls.items()), columns=['url', 'hash'])
        combined_df = pd.concat([all_urls_df, new_data_df]).drop_duplicates(subset=['url'])
        combined_df.to_csv('master.csv', index=False)
    print("Checkpoint saved.")

# Function to save visited URLs to a CSV file with current date and time in filename
def save_visited_urls_csv():
    """Save visited URLs to a CSV file with current date and time in filename."""
    global data_frame_1
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'visited_urls_{current_datetime}.csv'
    with visited_urls_lock:
        new_data_df = pd.DataFrame(list(visited_urls.items()), columns=['url', 'hash'])
        new_data_df.to_csv(filename, index=False)
    print(f"Visited URLs saved to {filename}")

# Worker function for crawling with uniqueness check
def worker(session, max_depth, delay):
    while True:
        current_url, depth = url_queue.get()
        if current_url is None:
            break

        if depth > max_depth:
            url_queue.task_done()
            continue

        print(f"[{current_thread().name}] Fetching {current_url}")
        html_content = fetch_page(session, current_url)
        time.sleep(delay)  # Delay between requests

        if html_content:
            url_hash = hashlib.sha256(current_url.encode()).hexdigest()
            with crawled_urls_lock:
                if current_url not in crawled_urls:
                    crawled_urls.add(current_url)

            with visited_urls_lock:
                if current_url not in visited_urls:
                    visited_urls[current_url] = url_hash

            if depth < max_depth:
                links = get_links(html_content, current_url)
                for link in links:
                    link_hash = hashlib.sha256(link.encode()).hexdigest()
                    with crawled_urls_lock:
                        if link not in crawled_urls:
                            crawled_urls.add(link)
                            url_queue.put((link, depth + 1))
                            with visited_urls_lock:
                                if link not in visited_urls:
                                    visited_urls[link] = link_hash

        else:
            print(f"[{current_thread().name}] Failed to retrieve {current_url}")

        url_queue.task_done()

# Function to crawl the website with uniqueness check
def crawl(url, max_depth, delay, num_threads):
    """Crawl the website starting from the given URL up to a maximum depth."""
    session = requests.Session()

    # Load the checkpoint if it exists
    load_from_sqlite()

    if url not in crawled_urls:
        url_queue.put((url, 0))

    threads = []
    for i in range(num_threads):
        thread = Thread(target=worker, args=(session, max_depth, delay), name=f"Thread-{i+1}")
        thread.start()
        threads.append(thread)

    # Wait for the queue to be empty
    url_queue.join()

    # Stop the threads
    for _ in range(num_threads):
        url_queue.put((None, 0))
    for thread in threads:
        thread.join()

    # After crawling is complete, save the checkpoint, visited URLs to CSV, and to SQLite
    save_checkpoint()
    save_visited_urls_csv()
    save_to_sqlite()

# Main function to start crawling and scraping
def main():
    url = "https://www.republicworld.com/"
    max_depth = 10
    delay = 1
    num_threads = 16

    print(f"Starting web crawling for {url}...")
    crawl(url, max_depth, delay, num_threads)

# Entry point of the script
if __name__ == "__main__":
    main()


# In[ ]:




