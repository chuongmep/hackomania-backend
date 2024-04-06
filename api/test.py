
from OpenAIImage import OpenAIImage

image_processor = OpenAIImage()
image_path_projector ="/Users/chuongmep/Downloads/projector.jpeg"
image_path_laptop ="/Users/chuongmep/Downloads/laptop.jpeg"
category = "Laptop"
result = image_processor.post_content_from_image(image_path_laptop,category)
print(result)