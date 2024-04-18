import json
from dotenv import load_dotenv
import os
import base64
from requests import post
import pandas as pd

# loads environment variable files
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# obtain access token
def get_token():
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

token = get_token()


# read csv file
df = pd.read_csv('train.csv')

# only use relavent cols
relevant_cols = [
    'track_id', 'artists', 'track_name', 'popularity', 'duration_ms',
    'danceability', 'energy', 'loudness', 'instrumentalness',
    'valence', 'tempo', 'track_genre'
]
df2 = df[relevant_cols].copy()

# get user input for mood
mood_input = input("Rate your mood (1-10): ")

# mood ranges for valence, energy, and dancabiliity
# may need to broaden ranges if not enough songs meet criteria
mood_ranges = {
    1: (0, 0.1),
    2: (0.1, 0.2),
    3: (0.2, 0.3),
    4: (0.3, 0.4),
    5: (0.4, 0.5),
    6: (0.5, 0.6),
    7: (0.6, 0.7),
    8: (0.7, 0.8),
    9: (0.8, 0.9),
    10: (0.9, 1)
}

# mood range for tempo
min_tempo = df2['tempo'].min()
max_tempo = df2['tempo'].max()
tempo_step = (max_tempo - min_tempo) / 10

tempo_ranges = {}
for i in range(1, 11):
    lower = min_tempo + (i - 1) * tempo_step
    upper = min_tempo + i * tempo_step
    tempo_ranges[i] = (lower, upper)
    
print(tempo_ranges)