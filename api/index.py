from http.server import BaseHTTPRequestHandler
from os.path import dirname, abspath, join

from api.OpenAIImage import OpenAIImage
dir = dirname(abspath(__file__))
import os
from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
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

@app.route("/api/get-content-image", methods=['POST'])
def get_content_image():
    oepnaimage = OpenAIImage()
    # add url to get image
    image_path = request.json.get('image_path')
    category = request.json.get('category')
    response = oepnaimage.post_content_from_image(image_path, category)
    response.headers['Content-Type'] = 'application/json'
    return response
# get content image from bytes 
@app.route("/api/get-content-image-bytes", methods=['POST'])
def get_content_image_by_bytes():
    oepnaimage = OpenAIImage()
    # add bytes image to body
    base64_image = request.json.get('base64_image')
    category = request.json.get('category')
    response = oepnaimage.post_content_from_bytes(base64_image, category)
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
        "In 2019, Singapore's total primary energy consumption was around 16 million tonnes of oil equivalent (Mtoe), which represented a 2.5% increase from 2018.",
        "The main sources of energy in Singapore's primary energy mix in 2019 were natural gas (95.2%) and others (4.8%), which included oil, coal, and renewable energy sources.",
        "Singapore has been actively pursuing renewable energy sources, particularly solar power, to diversify its energy mix. As of 2019, the country had around 350 megawatts (MW) of installed solar photovoltaic capacity.",
        "The building and transportation sectors are the largest energy consumers in Singapore, accounting for around 40% and 35% of total energy consumption respectively in 2019.",
        "Singapore has set a target to reduce its emissions intensity (emissions per unit of GDP) by 36% from 2005 levels by 2030, and to stabilize its greenhouse gas emissions with the aim of peaking around 2030."
    ]
    response = make_response(jsonify(facts))
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/api/openai_1', methods=['GET'])
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