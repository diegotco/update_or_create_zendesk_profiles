# The goal of this module is to create new users in Zendesk. 

import os
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

# Open the text file with all the users without a Zendesk profile.
with open("users_without_zd_profiles.txt", "r", encoding='utf-8-sig') as f:
    for line in f:
        if len(line) > 1:
            email_list.append(line.strip())

for email in email_list:

    # We are spliting the email in order to get the "username" that will work as a "name" further in the code.
    username = email.split("@")[0]

    # Load the user and the API Key from the .env file.
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value

    # Access the user.
    user = os.getenv("USER")

    # Access the API key.
    api_key = os.getenv("API_KEY")

    # Set the request parameters.
    url = f'https://{subdomain}.zendesk.com/api/v2/users'
    user = user + '/token'
    pwd = api_key

    # This dictionary will be sent to the server as a JSON object.
    # Very important: "email" and "name" variables are MANDATORIES.
    json_object = {
        "user": {
            "email": email,
            "verified": True,
            "name": username,
            "tags": [
                "vip"
                ],  
            "user_fields": {
                "vip_user": True
                }
        }
    }

    # Send the JSON object to the ZD server in order to create a profiles.
    try:
        response = requests.post(url, auth=(user, pwd), json=json_object)
    except:
        print("Something in the URL call or in the request module is wrong. Please check them.")
        exit()

    # Check for HTTP codes other than 201. # See here: https://developer.zendesk.com/api-reference/sales-crm/errors/#http-status-codes-summary
    if response.status_code != 201:
        
        # Status 201 means "Created" in ZD API.
        # The most probable reason to get an error is when a profile user was already created.
        print(f'User already exist or the email {email} is wrongly formated')

