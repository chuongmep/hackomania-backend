from http.server import BaseHTTPRequestHandler
import io
from os.path import dirname, abspath, join
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for Matplotlib
import matplotlib.pyplot as plt
import base64
import certifi


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
client = MongoClient(mongo_uri , tlsCAFile=certifi.where())
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

    return jsonify(data), 201


@app.route('/api/user', methods=['GET'])
def get_user_mongo():
    # Get the schema and data from the request
    data = request.json
    print("ABCD", request.json)
    users = db['users']
    user_id = data.get('user_id')
    print("XYY", user_id)
    user = users.find_one({'user_id': user_id})
    user['_id'] = str(user['_id'])
    # Insert the data into the new collection
    print("XB", user)

    return jsonify(user), 200


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
    file_storage = request.files.get('image_path')
    # The line `print("CHUONG", image_path.stream.read())` is reading the content of the file uploaded
    # as part of the request and printing it along with the string "CHUONG". This is useful for
    # debugging purposes to see the content of the file being processed in the `get_content_image`
    # endpoint.
    # print("CHUONG", image_path.stream.read())
    category = request.headers['category']
    stream = file_storage.stream.read()
    base64_image = base64.b64encode(stream)
    response = oepnaimage.post_content_from_bytes(base64_image, category)
    start = response.find('json') + 5
    end = response.rfind('}') + 1
    json_data = response[start:end]

    # Parse the JSON data
    data = json.loads(json_data)
    return data
# get content image from bytes 
@app.route("/api/get-content-image-bytes", methods=['POST'])
def get_content_image_by_bytes():
    oepnaimage = OpenAIImage()
    # add bytes image to body
    base64_image = request.files['base64_image']
    category = request.headers['category']
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
 
@app.route('/api/graph', methods=['POST'])
def get_user_graph():
    print(request.json)
    user_id = request.json.get('user_id')
    # Connect to MongoDB
    # Fetch data for the specified user
    user_data = db['users'].find_one({'user_id': user_id})

    if user_data:
        # Generate the graph using Matplotlib
        # Assume the data is in the format: [actual_value, projected_value]
        data = user_data['daily_projected_bill']
        data = [data * 1.25, data]
        print("ABCD", data)
        # Generate the graph using Matplotlib
        plt.figure(figsize=(8, 6))
        plt.bar([0, 1], data, color=['#4CAF50', '#E91E63'], width=0.4, edgecolor='#607D8B')
        plt.title(f"Daily Bill Projection", fontsize=16, fontweight='bold', color='#333333')
        plt.xlabel('', fontsize=14, color='#333333')
        plt.ylabel('Value ($)', fontsize=14, color='#333333')
        plt.xticks([0, 1], ['Actual', 'Projected'],  fontsize=12, color='#333333')

        # Save the graph to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # Convert the image to a base64-encoded string
        graph_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        # Return the graph as part of the API response
        return jsonify({'graph': graph_data})
    else:
        return jsonify({'error': f'User with ID {user_id} not found.'}), 404




#     def do_POST(self):
#       return
if __name__ == '__main__':
    app.run(debug=True)