#This file contains functions to interact with the Spotify API
#get_token() function retrieves an access token from spotify using OAuth2 athentication

#Track class is used to hold info for the two tracks in the game. get_rand_track_info() 
#method performs a search for 2 pseudorandom songs and stores info in object.

import random
import string
import requests
import json
import base64
from urllib.parse import urlencode

#Holds info regarding tracks
class Track:
    def __init__(self):
        pass

    def get_rand_track_info(self, token):
        #Fill auth field with valid token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        endpoint = "https://api.spotify.com/v1/search"

        #Very simple random search
        letter = random.choice(string.ascii_letters)

        #Finish lookup url
        data = urlencode({"q": f"{letter}", "type": "track"})
        lookup_url = f"{endpoint}?{data}"

        #Retrieve and store response of search
        r = requests.get(lookup_url, headers=headers)
        search_response_data = r.json()

        #Maximum random number allowed is determined
        max_num = len(search_response_data["tracks"]["items"])
        num = random.randint(0, max_num - 1)

        #Data extracted from response to variables
        self.track_name = search_response_data["tracks"]["items"][num]["name"]
        self.artist_name = search_response_data["tracks"]["items"][num]["artists"][0]["name"]
        self.album_name = search_response_data["tracks"]["items"][num]["album"]["name"]
        self.song_popularity = search_response_data["tracks"]["items"][num]["popularity"]
        self.cover_art_url = search_response_data["tracks"]["items"][num]["album"]["images"][0]["url"]


#Send request to spotify accounts service for access token
def get_token():
    #Personal id and secret retrieved from json file
    #Needed to make a request for token
    with open('clientInfo.json') as clientInfo:
        data = json.load(clientInfo)

    client_id = data['client_id']
    client_secret = data['client_secret']

    #Create and encode elements needed in request
    client_creds = f"{client_id}:{client_secret}"

    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    token_url = "https://accounts.spotify.com/api/token"

    token_data = {
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Authorization": f"Basic {client_creds_b64}"
    }

    #Send request
    r = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = r.json()

    #Store access token from response
    access_token = token_response_data['access_token']

    return access_token
