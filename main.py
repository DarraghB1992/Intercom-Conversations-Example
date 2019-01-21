from ratelimit import limits
import requests
import os

accessToken = os.environ('IntercomAccessToken')

# Base URL to request Conversations
intercomUrl = 'https://api.intercom.io/conversations'

headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + accessToken}

# Maximum amount of conversations per page is 60
params = {'per_page': 60}


@limits(calls=83, period=60)
def get_conversations():
    response = requests.get(intercomUrl, headers=headers, params=params)
    first_call_json = response.json()
    current_page = first_call_json['pages']['page']
    total_pages = first_call_json['pages']['total_pages']
    next_page_url = first_call_json['pages']['next']

    # Loop through the rest of the pages
    while current_page < total_pages:
        r = requests.get(next_page_url, headers=headers, params=params)
        conversation_json = r.json()

        current_page = conversation_json['pages']['page']
        total_pages = conversation_json['pages']['total_pages']
        next_page_url = conversation_json['pages']['next']

        # Do things with the conversation json

        if r.status_code != 200:
            raise Exception('Api response: {}'.format(r.status_code))

        print r.text


get_conversations()
