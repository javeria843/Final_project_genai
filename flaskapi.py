from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('user_input', '').lower()

    # Simple rule-based responses
    if "top dishes" in user_input:
        reply = "Our top dishes are chicken biryani and lamb karahi."
    elif "location" in user_input:
        reply = "We're located in Gulshan-e-Iqbal, Karachi."
    elif "prices" in user_input:
        reply = "Our prices of dishes start from 1000 PKR."
    else:
        reply = "Sorry, I didn't understand your question."

    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(debug=True)
