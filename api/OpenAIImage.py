import base64
import requests
import json
import os
class OpenAIImage:
    def __init__(self):
        self.api_key = os.environ.get("OPEN_API_KEY")

    @staticmethod
    def encode_image(image):
        base64.b64encode(image).decode('utf-8')

    
    @staticmethod
    def _is_file_exist(file_path):
        try:
            with open(file_path, 'r') as file:
                return True
        except FileNotFoundError:
            return False

    @staticmethod
    def read_json(file_path):
        flag = OpenAIImage._is_file_exist(file_path)
        if not flag:
            print(f"File '{file_path}' does not exist.")
            return None
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def get_text_by_category(prompt_data, category):
        for item in prompt_data:
            if item["category"] == category:
                return item["text"]
        return None

    def post_content_from_image(self, image, category):
        base64_image = OpenAIImage.encode_image(image)
        return self.post_content_from_bytes(base64_image, category)
        
    def post_content_from_bytes(self, base64_image, category):
        # fix prompt_path from api/data/promt.json
        # get folder data same directory with  api 
        prompt_path = os.path.join(os.path.dirname(__file__),"..", 'data', 'prompt.json')
        print(prompt_path)
        prompt_data = OpenAIImage.read_json(prompt_path)
        selected_text = OpenAIImage.get_text_by_category(prompt_data, category)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
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
                                "url": f"data:image/jpeg;base64,{base64_image.decode('utf-8')}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']

