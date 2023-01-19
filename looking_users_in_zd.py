# The goal of this module is to look up for users IDs in Zendesk.
# A text file with all users email is required. 

import os
from urllib.parse import urlencode
import requests


# Zendesk subdomain. 
subdomain = '' # For example: acme.zendesk.com. Your company set it.

# Load the user and the API Key from the .env file.
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value

# Access the user.
user = os.getenv("USER")

# Access the API key.
api_key = os.getenv("API_KEY")

# Users email list that we will be getting from a text file.
email_list = []

# Open the text file with all the vip email users on it.
with open("vip_email_users.txt", "r", encoding='utf-8-sig') as f:
    for line in f:
        if len(line) > 1:
            email_list.append(line.strip())

# For saving the users Zendesk IDs.
id_list = []

# For saving data that are producing errors while searching for the users IDs.
wrong_data = []

for email in email_list:

    # Load the user and the API Key from the .env file.
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value

    # Access the user.
    user = os.getenv("USER")

    # Access the API key.
    api_key = os.getenv("API_KEY")
    
    params = {
        # Query for specific user's email.
        'query': f'type:user email:{email}'
    }

    # Set the request parameters.
    url = f'https://{subdomain}.zendesk.com/api/v2/search.json?' + urlencode(params)
    user = user + '/token'
    pwd = api_key

    # Do the HTTP get request with try/except.
    try:
        response = requests.get(url, auth=(user, pwd))
    except:
        print("Something in the URL call or in the request module is wrong. Please check them.")
        exit()

    # Check for HTTP codes other than 200.
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data.
    data = response.json()

    # If the value is not an email that could raise an error, e.g an phon number. We are saving these values for further analysis. 
    try:
        zd_id_user = data["results"][0]["id"]
        id_list.append(zd_id_user)
    except:
        wrong_data.append(email)
    
# Saving the ZD users in a text file.
with open('zd_id_users.txt', 'a') as f:
    for id in id_list:
        f.write(str(id) + "\n")

# Saving the wrong data in a text file.
with open('wrong_data.txt', 'a') as f:
    for data in wrong_data:
        f.write(str(data) + "\n")
