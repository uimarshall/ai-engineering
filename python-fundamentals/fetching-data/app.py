import json
from urllib import request

import requests
from rich import print, print_json

# https://jsonplaceholder.typicode.com/posts


# fetch data from a URL using urllib and parse the JSON response
def fetch_data(url):
    try:
        with request.urlopen(url) as response:
            data = response.read()
            parsed_json = json.loads(data)
            return parsed_json
    except Exception as e:
        print(f"[bold red]Error fetching data: {e}[/bold red]")
        return None


# Fetch data using requests library as alternative to urllib
def fetch_data_requests(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        parsed_json = response.json()
        return parsed_json
    except requests.exceptions.RequestException as e:
        print(f"[bold red]Error fetching data with requests: {e}[/bold red]")
        return None


def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    users_url = "https://jsonplaceholder.typicode.com/users"
    posts = fetch_data(url)
    if posts:
        # print the fetched JSON data in a pretty format using rich
        print("[bold green]Fetched Posts:[/bold green]")
        print_json(data=posts)

    users = fetch_data_requests(users_url)
    if users:
        # print the fetched JSON data in a pretty format using rich
        print_json(data=users)


if __name__ == "__main__":
    main()
