from flask import Flask, request, jsonify
import base64
import requests
import json

app = Flask(__name__)

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

@app.route('/api/openai/base64', methods=['POST'])
def openai_api_base64():
    # Get the category and image bytes from the request headers
    category = request.headers.get('Category')
    image_bytes = request.get_data()

    # Getting the base64 string
    base64_image = encode_image(image_bytes)

    # Path to your prompt data
    prompt_path = "/path/to/prompt.json"

    # Function to read JSON data from a file
    def read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    # Function to retrieve text based on category
    def get_text_by_category(data, category):
        for item in data:
            if item["category"] == category:
                return item["text"]
        return None

    # Read JSON data
    prompt_data = read_json(prompt_path)
    # Example usage
    selected_text = get_text_by_category(prompt_data, category)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{selected_text}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Return the response content as JSON
    return jsonify(response.json()['choices'][0]['message']['content'])

@app.route('/api/openai/file', methods=['POST'])
def openai_api_file():
    # Get the category from the request headers
    category = request.headers.get('Category')

    # Get the image file path from the request body
    image_path = request.get_data().decode('utf-8').strip()

    # Function to encode the image
    def encode_image_from_file(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string from file
    base64_image = encode_image_from_file(image_path)

    # Path to your prompt data
    prompt_path = "/path/to/prompt.json"

    # Function to read JSON data from a file
    def read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    # Function to retrieve text based on category
    def get_text_by_category(data, category):
        for item in data:
            if item["category"] == category:
                return item["text"]
        return None

    # Read JSON data
    prompt_data = read_json(prompt_path)
    # Example usage
    selected_text = get_text_by_category(prompt_data, category)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{selected_text}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Return the response content as JSON
    return jsonify(response.json()['choices'][0]['message']['content'])
