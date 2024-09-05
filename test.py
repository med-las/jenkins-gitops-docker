import requests

def check_internal_server_error(url, session):
    """
    Check if the Odoo server at the given URL is running fine and not returning a 500 Internal Server Error.

    :param url: The URL to check (e.g., "http://localhost:8069/web").
    :param session: A requests.Session object to use for making the request.
    :return: None. Prints out the status of the server.
    """
    try:
        # Send a GET request to the Odoo server
        response = session.get(url)

        # Check if the server responded with a 500 Internal Server Error
        if response.status_code == 500:
            print("Internal Server Error (500): The server encountered an error.")
        elif response.status_code == 200:
            print("Server is running fine.")
        else:
            print(f"Server returned status code {response.status_code}.")
    
    except requests.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Odoo server URL
    odoo_url = "http://localhost:8069/web"
    
    # Create a requests session
    session = requests.Session()

    # Check the Odoo server
    check_internal_server_error(odoo_url, session)
