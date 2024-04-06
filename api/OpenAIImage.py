import base64
import requests
import json
class OpenAIImage():
    def __init__(self):
        self.api_key = "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"

    def encode_image(image_bytes):
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def _is_file_exist(file_path):
        try:
            with open(file_path, 'r') as file:
                return True
        except FileNotFoundError:
            return False
    # Function to read JSON data from a file
    def read_json(file_path):
        flag = self._is_file_exist(file_path)
        if not flag:
            print(f"File '{file_path}' does not exist.")
            return None
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    # Function to retrieve text based on category
    def get_text_by_category(prompt_data, category):
        for item in prompt_data:
            if item["category"] == category:
                return item["text"]
        return None
    def post_content_from_image(image_path,category):
        prompt_path = "../data/api/prompt.json"
        prompt_data = self.read_json(prompt_path)
# Example usage
        selected_text = self.get_text_by_category(prompt_data, category)

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.api_key}"
        }
        base64_image = self.encode_image(image_path)
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

        # print(response.json())
        response.json()['choices'][0]['message']['content']
