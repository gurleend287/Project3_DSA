from flask import Flask, request, jsonify
import playlist

app = Flask(__name__)

@app.route("/members")
def members():
    return "bobita"
    #return{"members": ["Member1", "Member2", "Member3"]}

@app.route("/send_rating", methods=['POST'])
def receive_rating():
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
    
    # user input
    # mood_input, playlist_size, search_input = playlist.get_user_input()

    # thesholds based on mood input
    threshold_map = playlist.define_thesholds(ranges_map, mood_input)

    graph = playlist.build_graph(df, playlist_size, criteria, threshold_map)

    # creates csv files based on search algo chosen
    playlist.perform_search(graph, search_input)

    # Process the rating (For demonstration, just returning it back)
    response = f"Received rating: {rating}"

    return jsonify({'response': response})

@app.route('/get_csv_data')
def get_csv_data():
    # Read the CSV file here
    filename = request.args.get('file_name')
    # For this example, I'm assuming dfs.csv and bfs.csv are in the same directory
    with open(filename, 'r') as file:
        data = [line.strip().split(',') for line in file.readlines()]
    return jsonify(data)

def get_graph_data():
    # Generate and return graph data (nodes and links) here
    # For example:
    graph_data = {
        "nodes": [
            {"id": "node1"},
            {"id": "node2"},
            # Add more nodes as needed
        ],
        "links": [
            {"source": "node1", "target": "node2"},
            # Add more links as needed
        ]
    }
    
    return jsonify(graph_data)



if __name__ == "__main__":
    app.run(debug=True)
     