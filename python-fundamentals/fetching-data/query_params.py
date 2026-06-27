import requests
from rich import print, print_json


# Fetch data using requests library as alternative to urllib
def fetch_data_requests(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        parsed_json = response.json()
        return parsed_json
    except requests.exceptions.RequestException as e:
        print(f"[bold red]Error fetching data with requests: {e}[/bold red]")
        return None


def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    users_url = "https://jsonplaceholder.typicode.com/users"
    query_params = {
        "userId": 1,
        "_limit": 5,
    }  # Example query parameter to filter posts by userId

    # Fetch data with query parameters (fetch only 5 posts for userId=1)
    posts = fetch_data_requests(
        url, params=query_params
    )  # fetch only 5 posts for userId=1
    if posts:
        # print the fetched JSON data in a pretty format using rich
        print("[bold green]Fetched Posts:[/bold green]")
        print_json(data=posts)

    users = fetch_data_requests(users_url)
    if users:
        # print the fetched JSON data in a pretty format using rich
        print("[bold green]Fetched Users:[/bold green]")
        print_json(data=users)


if __name__ == "__main__":
    main()
