import requests

def authenticate_odoo(url, db, username, password):
    login_url = f"{url}/web/session/authenticate"

    payload = {
        'jsonrpc': '2.0',
        'params': {
            'db': db,
            'login': username,
            'password': password
        }
    }
    
    response = requests.post(login_url, json=payload)
    
    if response.status_code == 200 and response.json().get('result'):
        session_id = response.cookies.get('session_id')
        return session_id
    else:
        print("400")
        return None

def check_internal_server_error(url, session_id):
    headers = {
        'Cookie': f'session_id={session_id}'
    }

    try:
        response = requests.get(url, headers=headers)

        if "Internal Server Error" not in response.text:
            print("200")
        else:
            print("400")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


# -------------------------------------------------------------------------------------------------------

odoo_url = "http://localhost:8069"
odoo_db = "internship_jul_sep"  
odoo_username = "admin"
odoo_password = "admin"

session_id = authenticate_odoo(odoo_url, odoo_db, odoo_username, odoo_password)

if session_id:
    check_internal_server_error(f"{odoo_url}/web", session_id)