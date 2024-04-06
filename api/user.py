from http.server import BaseHTTPRequestHandler
from os.path import dirname, abspath, join
dir = dirname(abspath(__file__))


import os
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
mongo_uri = "mongodb+srv://chuongpqvn:YIxK7JNeOdB2TvHz@hack-omania.igeosd7.mongodb.net/?retryWrites=true&w=majority&appName=hack-omania"
client = MongoClient(mongo_uri)
db = client.your_database_name

@app.route('/api/create', methods=['POST'])
def create_api():
    # Get the schema and data from the request
    schema = request.json.get('schema')
    data = request.json.get('data')

    # Create a new collection based on the schema
    collection_name = schema['name']
    collection = db[collection_name]

    # Insert the data into the new collection
    collection.insert_one(data)

    return jsonify({'message': 'API created successfully'}), 201
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        with open(join(dir, '..', 'data', 'user.json'), 'r') as file:
          for line in file:
            self.wfile.write(line.encode())
        return



    def do_POST(self):
      return