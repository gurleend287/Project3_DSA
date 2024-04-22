from flask import Flask, request, jsonify
from main import create_graph, test_traversal

app = Flask(__name__)

@app.route("/members")
def members():
    return "bobita"
    #return{"members": ["Member1", "Member2", "Member3"]}

@app.route("/send_rating", methods=['POST'])
def receive_rating():
    data = request.get_json()
    rating = data.get('rating')
    
    # Store the rating in a variable
    # app.rating = rating

    rating_num= int(rating)
    print("______")
    print(rating_num)
    print("______")

    graph = create_graph(rating_num)
    test_traversal(graph)

    # Process the rating (For demonstration, just returning it back)
    response = f"Received rating: {rating}"

    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=True)
     