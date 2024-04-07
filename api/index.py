from http.server import BaseHTTPRequestHandler
import io
from os.path import dirname, abspath, join
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for Matplotlib
import matplotlib.pyplot as plt
import base64
import certifi
import numpy as np

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
    data_list = request.json.get('devices')
    print("ABCD", request.json)
    users = db['users']
    user_id = request.json.get('user_id')
    # if user_if not found, create new user
    if not users.find_one({'user_id': user_id}):
        users.insert_one(request.json)
    print("XYY", user_id)
    user = users.find_one({'user_id': user_id})
    _id = user.get('_id')
    user['number_of_devices'] = 0
    user['daily_projected_bill'] = 0.0
    # check if any device is new on data_list not in user['devices'], add it to user['devices']
    for data in data_list:
        if data not in user['devices']:
            print("Data Not in user['devices']", data)
            user['devices'].append(data)
    for device in user['devices']:
        for data in data_list:
            if device['name'] == data['name'] and data['status'] == True:
                device['kwh'] = data['kwh']
                device['status'] = True
                device['hours'] = data['hours']
                user['number_of_devices'] += 1
                user['daily_projected_bill'] += user['cost_per_kwh'] * data['hours'] * data['kwh']
    users.update_one({'_id': _id}, {'$set': user})
    user['_id'] = str(user['_id'])
    for device in user['devices']:
        if device['name'] == data['name']:
            device['kwh'] = data['kwh']
    print("XAA", user)

    response = make_response(user)
    response.headers['Content-Type'] = 'application/json'

    return response
@app.route('/api/delete-device', methods=['POST'])
def delete_projector():
    # Get the schema and data from the request
    data = request.json
    print("ABCD", request.json)
    users = db['users']
    user_id = data.get('user_id')
    print("XYY", user_id)
    user = users.find_one({'user_id': user_id})
    devices = user.get('devices')
    device_name = "Projector"
    # delete device with name "Projector"
    for device in devices:
        if device['name'] == device_name:
            devices.remove(device)
    user['devices'] = devices
    _id = user.get('_id')
    users.update_one({'_id': _id}, {'$set': user})
    user['_id'] = str(user['_id'])
    print("XAA", user)
    return jsonify(user), 200
@app.route("/api/get-content-image", methods=['POST'])
def get_content_image():
    oepnaimage = OpenAIImage()
    # add url to get image
    file_storage = request.files.get('image_path')
    print("file_storage:", file_storage)
    # The line `print("CHUONG", image_path.stream.read())` is reading the content of the file uploaded
    # as part of the request and printing it along with the string "CHUONG". This is useful for
    # debugging purposes to see the content of the file being processed in the `get_content_image`
    # endpoint.
    # print("CHUONG", image_path.stream.read())
    category = request.headers['category']
    stream = file_storage.stream.read()
    base64_image = base64.b64encode(stream)
    response = oepnaimage.post_content_from_bytes(base64_image, category)
    print("ABCD", response)
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
    
    
@app.route('/api/anomaly/graph', methods=['POST'])
def get_user_anomaly_graph():
    print(request.json)
    # Array of values
    data = [1.44, 1.27, 1.45, 1.21, 1.38, 1.16, 1.16, 1.06, 1.08, 1.07, 1.09, 1.42, 1.26, 1.02, 1.15, 1.09, 1.02, 1.1, 1.03, 1.29, 1.31, 1.32, 1.4, 1.41, 1.35, 1.11, 1.01, 1.09, 1.47, 1.15, 1.28, 1.47, 1.06, 1.28, 1.43, 1.43, 1.24, 1.29, 2.91, 2.81, 3.3, 2.85, 2.94]

    # X-axis ticks and labels
    x_ticks = np.arange(0, len(data) * 0.5, 0.5)
    x_labels = ['12 AM', '', '', '', '', '', '', '', '', '', '5 AM', '', '', '', '', '', '', '', '', '', '10 AM', '', '', '', '', '', '', '', '', '', '3 PM', '', '', '', '', '', '', '', '', '', '8 PM', '', '']
# Color for the last 4 bars
    last_4_bars_color = 'red'

    # List of colors for all the bars
    colors = ['#c9f4eb'] * (len(data) - 5) + [last_4_bars_color] * 5

    # Plotting the bar plot
    plt.bar(x_ticks, data, color=colors, alpha=0.76, width=0.4)

    # Setting the title and labels
    plt.title('Energy Consumption Bar Plot', fontsize=18)
    plt.xlabel('Half Hourly', fontsize=16)
    plt.ylabel('kWh', fontsize=16)

    # Setting the X-axis ticks and labels
    plt.xticks(x_ticks, x_labels, rotation=90, fontsize=7)
    plt.ylim(0, max(data))
    # Save the graph to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Convert the image to a base64-encoded string
    graph_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    # Display the plot
    return jsonify({'graph': graph_data})  




#     def do_POST(self):
#       return
if __name__ == '__main__':
    app.run(debug=True)