import json
from dotenv import load_dotenv
import os
import base64
from requests import post
import pandas as pd
from node import Node
from graph import Graph

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

# mood ranges for valence, energy, and dancabiliity
# may need to broaden ranges/overlap if not enough songs meet criteria
criteria = ['danceability', 'energy', 'valence', 'tempo']
ranges_map = {}

for col in criteria:
    min  = df2[col].min()
    max = df2[col].max()
    step = (max - min) / 10
    
    ranges = {}
    for i in range(1,11):
        lower = min + (i - 1) * step
        upper = max + i * step
        ranges[i] = (lower, upper)
        
    ranges_map[col] = ranges
    
# get user input for mood
mood_input = input("Rate your mood (1-10): ")

# set thresholds based on chosen mood
threshold_map = {}
for key, ranges in ranges_map.items():
    threshold_map[key] = ranges.get(int(mood_input))

print(threshold_map)
    
# test node class
first = df2.iloc[0].to_dict()
node1 = Node(**first)
second = df2.iloc[1].to_dict()
node2 = Node(**second)

# # test graph class
# adj_list = Graph(threshold_map)
# cols = ['valence', 'energy']
# adj_list.add_node(node1, cols)
# print(adj_list)