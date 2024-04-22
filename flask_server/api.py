import base64
import json
from requests import post, get

# obtain access token
def get_token(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    
    return token

# create header using access token for requests
def get_auth_header(token):
     return {"Authorization": "Bearer " + token}

# some track_names not given in viable format
# get track_details
def get_track_details(token, track_id: str):
    url = "https://api.spotify.com/v1/tracks/"
    headers = get_auth_header(token)
    query_url = url + track_id
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    # get details: image url, track name, track url
    image_url = json_result['album']['images'][1]['url']
    track_name = json_result['name']
    track_url = json_result['external_urls']['spotify']
    artist = json_result['artists'][0]['name']
    
    return image_url, track_name, track_url, artist

