import requests
from rich import print, print_json

# POST requests

def post_data_requests(url, data=None):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        parsed_json = response.json()
        return parsed_json
    except requests.HTTPError as http_err:
        print(f"[bold red]HTTP error occurred: {http_err}[/bold red]")
        return None  
    except requests.exceptions.RequestException as e:
        print(f"[bold red]Error posting data with requests: {e}[/bold red]")
        return None
      
def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    post_data = {
        "title": "Empty",
        "body": "barrel makes the loudest noise",
        "userId": 1,
    }  # Example data to be sent in the POST request

    # Post data to the API
    # Once the data is posted, the API will return a response with the created resource, including an ID.
    response_data = post_data_requests(url, data=post_data)
    if response_data:
        # print the response JSON data in a pretty format using rich
        print("[bold green]Response from POST request:[/bold green]")
        
        print_json(data=response_data)
        if response_data.get("id"):
            print(f"[bold blue]New post created with ID: {response_data['id']}[/bold blue]")
            
if __name__ == "__main__":
    main()      