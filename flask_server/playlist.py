import os
import pandas as pd
from graph import Graph
from node import Node
import csv
import api

# read and process csv file into df
def process_data():
    # read csv file
    df = pd.read_csv('train.csv')

    # only use relavent cols
    relevant_cols = [
        'track_id', 'artists', 'track_name', 'popularity', 'duration_ms',
        'danceability', 'energy', 'loudness', 'instrumentalness',
        'valence', 'tempo', 'track_genre'
    ]
    df = df[relevant_cols].drop_duplicates(subset=['track_name'])
    return df

# pandas dataframe when passed as a parameter will be modified w/o making copy
# build value ranges for each criteria
def criteria_ranges(df, criteria: list[str], num_ranges: int):
    ranges_map = {}

    for col in criteria:    
        min  = df[col].min()
        max = df[col].max()
        step = (max - min) / num_ranges
    
        ranges = {}
        for i in range(1,1 + num_ranges):
            lower = min + (i - 1) * step
            upper = min + i * step
            ranges[i] = (lower, upper)
        
        ranges_map[col] = ranges
    
    return ranges_map

# set thresholds for each criteria based on chosen mood
def define_thesholds(ranges_map: dict, mood_input: int):
    threshold_map = {}
    for key, ranges in ranges_map.items():
        threshold_map[key] = ranges.get(int(mood_input))
    return threshold_map

# get user input for mood, playlise size, and search algo
def get_user_input():
    mood_input = input("Rate your mood (1-5): ")
    playlist_size = input("Enter the size of your playlist (1-100): ") # traversal returns less than size since not all nodes connected
    search_input = input("Select a search algorithm (1-BFS or 2-DFS): ")
    return int(mood_input), int(playlist_size), int(search_input)

# build graph using adjacency list based on user inputs
def build_graph(df, playlist_size: int, criteria: list[str], threshold_map: dict):
    graph = Graph(threshold_map)

    # parse through first half of dataset
    # add nodes based on tempo and valence only
    cols1 = ['valence', 'tempo']
    for i, row in df.iloc[:len(df)//2].iterrows():
        curr_node = Node(**row.to_dict())
        if(graph.size < 250):
            graph.add_node(curr_node, cols1)

    # parse through second half of dataset
    # add nodes based on all 4 criteria
    for i, row in df.iloc[len(df)//2:].iterrows():
        curr_node = Node(**row.to_dict())
        if(graph.size < 250): # ensure graph does not exceed size of max playlist
            graph.add_node(curr_node, criteria)
    
    # add edges between nodes
    keys = list(graph.adj_list.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            graph.add_edge(keys[i][1], keys[j][1])

    return graph


# perform picked search algorithm
def perform_search(graph: Graph, search_input: int):
    start_node = next(iter(graph.adj_list.keys()))[1]

    # bfs
    if (search_input == 1):
        graph.bfs(start_node)

    # dfs
    elif (search_input == 2):
        # remove existing file
        if os.path.exists("dfs.csv"):
            os.remove("dfs.csv")
        # write header to new csv file
        with open('dfs.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['track_id', 'popularity', 'duration_ms', 'danceability',
                             'energy', 'loudness', 'instrumentalness', 'valence', 'tempo', 'track_genre'])
        graph.dfs(start_node)

# find average of given characters
def average_val(file_name, characteristics: list[str], playlist_size: int):
    try:
        # read csv and cut off at playlist_size
        df = pd.read_csv(file_name)
        df = df[characteristics]
        df = df.head(playlist_size)
        # create dict of averages (keys are col names)
        averages = df.mean().to_dict()
        return averages
    except FileNotFoundError:
        print(f"File '{file_name}' not found")
        return None

# modify playlist df to include track_name, track_image_url, and track_url
def add_track_details(df, playlist_size: int, token):
    image_urls = []
    track_names = []
    track_urls = []
    artists = []

    for track_id in df['track_id'].head(playlist_size):
        # get track details using api
        image_url, track_name, track_url, artist = api.get_track_details(token, track_id)
        
        image_urls.append(image_url)
        track_names.append(track_name)
        track_urls.append(track_url)
        artists.append(artist)

    # add to df
    df['track_image_url'] = image_urls
    df['track_name'] = track_names
    df['track_url'] = track_urls
    df['artists'] = artists

    return df
        
