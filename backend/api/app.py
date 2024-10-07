import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# https://www.moesif.com/blog/technical/api-development/Building-RESTful-API-with-Flask/

app = Flask(__name__)
CORS(app)
# to customize which domains are allowed to access the app
# CORS(app, resources={r"/api/*": {"origins": "http://example.com"}})

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from Flask API!'}
    return jsonify(data)


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True)