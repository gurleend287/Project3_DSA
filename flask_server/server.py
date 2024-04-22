from flask import Flask, request, jsonify
import playlist
import pandas as pd
import api
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/send_rating", methods=['POST'])
def receive_rating():
    # loads environment variable files
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    token = api.get_token(client_id, client_secret)

    data = request.get_json()
    rating = data.get('rating')
    textInput = data.get('textInput')
    radioOption = data.get('radioOption')
    
    # Store the rating in a variable
    # app.rating = rating

    mood_input= int(rating)
    playlist_size=int(textInput)
    search_input_str= str(radioOption)
    search_input = None

    if (search_input_str == "option1"):
        search_input=1
    if (search_input_str == "option2"):
        search_input=2

    print("______") 
    print(mood_input)
    print(playlist_size)
    print(search_input)
    print("______") 

    df = playlist.process_data()
    criteria = ['danceability', 'energy', 'valence', 'tempo']

    # mood ranges for valence, energy, dancabiliity, and tempo
    # may need to broaden ranges/overlap if not enough songs meet criteria
    ranges_map = playlist.criteria_ranges(df, criteria, num_ranges=5)
    
    # user input - command line
    # mood_input, playlist_size, search_input = playlist.get_user_input()

    # thesholds based on mood input
    threshold_map = playlist.define_thesholds(ranges_map, mood_input)

    graph = playlist.build_graph(df, playlist_size, criteria, threshold_map)

    # creates csv files based on search algo chosen
    playlist.perform_search(graph, search_input)

    # averages stats for playlist
    if (search_input == 1):
        file_name = 'bfs.csv'
    elif (search_input == 2):
        file_name = 'dfs.csv'
    average_cols = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'instrumentalness']
    # returns dict of averages
    average_dict = playlist.average_val(file_name, average_cols, playlist_size)

    # build playlist df based on input
    playlist_df = pd.read_csv(file_name)

    # add track details
    playlist_df = playlist.add_track_details(playlist_df, playlist_size, token)

    # remove existing file
    if os.path.exists("final_playlist.csv"):
        os.remove("final_playlist.csv")

    # write csv file for playlist
    playlist_df.to_csv('final_playlist.csv', index=False)

    # Process the rating (For demonstration, just returning it back)
    response = f"Received rating: {rating}"

    return jsonify({'response': response})

@app.route('/get_csv_data')
def get_csv_data():
    with open('final_playlist.csv', 'r') as file:
        data = [line.strip().split(',') for line in file.readlines()]
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
     