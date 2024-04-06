from http.server import BaseHTTPRequestHandler
from os.path import dirname, abspath, join
dir = dirname(abspath(__file__))
import os
from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from OpenAIImage import OpenAIImage
import json

app = Flask(__name__)

# Connect to MongoDB
mongo_uri = "mongodb+srv://chuongpqvn:YIxK7JNeOdB2TvHz@hack-omania.igeosd7.mongodb.net/?retryWrites=true&w=majority&appName=hack-omania"
client = MongoClient(mongo_uri)
db = client.your_database_name

@app.route('/api/create', methods=['POST'])
def create_api():
    # Get the schema and data from the request
    data = request.json
    print("ABCD", request.json)
    # Create a new collection based on the schema
    collection = db['users']

    # Insert the data into the new collection
    print("XB", collection.insert_one(data))

    return jsonify({'message': 'API created successfully'}), 201


@app.route('/api/add-device', methods=['POST'])
def add_device():
    data = request.json
    print("ABCD", request.json)
    users = db['users']
    user_id = data.get('user_id')
    print("XYY", user_id)
    user = users.find_one({'user_id': user_id})
    _id = user.get('_id')
    user.get('devices').append(request.json.get('device'))
    users.update_one({'_id': _id}, {'$set': user})
    user['_id'] = str(user['_id'])
    
    print("XAA", user)

    response = make_response(user)
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route("api/get-content-image", methods=['POST'])
def get_content_image():
    oepnaimage = OpenAIImage()
    # add url to get image
    image_path = request.json.get('image_path')
    category = request.json.get('category')
    response = oepnaimage.post_content_from_image(image_path, category)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/user', methods=['GET'])
def get_user():
    with open(join(dir, '..', 'data', 'user.json'), 'r') as file:
        a = file.readlines()
        response = make_response((''.join(a)))
        response.headers['Content-Type'] = 'application/json'
        return response
    

@app.route('/api/green-energy-fact', methods=['GET'])
def get_green_energy_facts():
    facts = [
        {
            "fact": "Wind power is one of the fastest-growing renewable energy sources, with global installed capacity increasing from 7.5 gigawatts (GW) in 1997 to over 650 GW in 2019.",
            "source": "International Energy Agency"
        },
        {
            "fact": "Solar energy is the fastest-growing renewable energy source, with the global installed capacity increasing from just 7 GW in 2007 to over 580 GW in 2019.",
            "source": "International Renewable Energy Agency"
        },
        {
            "fact": "Renewable energy sources, such as wind, solar, and hydropower, accounted for around 26% of the global electricity generation in 2019.",
            "source": "International Energy Agency"
        }
    ]
    response = make_response(jsonify(facts))
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/api/openai', methods=['GET'])
def openai():
    return "Chuong is a great guy!!!1"
 
# class handler(BaseHTTPRequestHandler):
 
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/plain')
#         self.end_headers()
#         with open(join(dir, '..', 'data', 'user.json'), 'r') as file:
#           for line in file:
#             self.wfile.write(line.encode())
#         return



#     def do_POST(self):
#       return
if __name__ == '__main__':
    app.run(debug=True)