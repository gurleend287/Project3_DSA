from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/members")
def members():
    return{"members": ["Member1", "Member2", "Member3"]}


@app.route('/send_rating', methods=['POST'])
def send_rating():
    data = request.json
    rating = data.get('rating')
    
    # You can now use the rating value as needed
    print(f"Received rating: {rating}")
    
    # For demonstration purposes, let's return a response
    return jsonify({"response": f"Received rating: {rating}"}), 200


if __name__ == "__main__":
    app.run(debug=True)
     