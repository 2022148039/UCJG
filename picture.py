import os
import cv2
import requests
import numpy as np
import re
from matplotlib import pyplot as plt
import base64
# Function to encode the image
def encode_image(image_path):
    image = cv2.imencode('.png', cv2.imread(image_path))[1]
    return base64.b64encode(image).decode('utf-8')

# Set the api_key and headers for OpenAI API
api_key = "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"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Function to adjust image using OpenAI API
def adjust_image(image_path):
    base64_image = encode_image(image_path)
    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": """
            First, Decide which of the following is a landscape painting figure painting still life painting croquis abstract portrait. Analyze the image and suggest recommendations on how to adjust Hue, Saturation, and Value (HSV) to enhance its overall appearance to me.
            if Value should be increase by 10, please say value:+10 . if saturation value should be incerese by 10, please say saturation: +10. if Value should be increase by 10, please say Value: +10. if each value should be decrease, please say -10.    
            If there is no need to change the value, please say Value: +0.
            Second, Please recommend the RGB value of the light that makes visible like the photo corrected when the light is illuminated Following to this format :  'R : num, G : num, B: num' You must suggest R,G,B value all.""
            """            
            
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
          ]
     }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_message = response.json()['choices'][0]['message']['content']

    # Print the response
    print(response_message.encode('cp949', 'replace').decode('cp949'))

    # Define patterns for each element
    patterns = {'hue': r'Hue:\s*([+\-]?\d+(?:\.\d+)?)', 'saturation': r'Saturation:\s*([+\-]?\d+(?:\.\d+)?)', 'value': r'Value:\s*([+\-]?\d+(?:\.\d+)?)'}
    hsv_values = {'Hue': 0, 'Saturation': 0, 'Value': 0}

    # Update dictionary creation
    for k, p in patterns.items():
        match = re.search(p, response_message)
        if match:
            hsv_values[k.capitalize()] = int(match.group(1))
        
    print(hsv_values)


    # 정규표현식을 사용하여 R, G, B 값을 추출
    rgb_pattern = r'(R|G|B)\s*:\s*(\d+)'

    # Use the regex to find all matching RGB values
    matches = re.findall(rgb_pattern, response_message)

    # If matches found, print the RGB values
    if matches:
        rgb_values = {k: int(v) for k, v in matches}  # change from 'gb_values' to 'rgb_values'
        with open('rgb.txt', 'a') as f:
            f.write(f"'{os.path.basename(image_path)}' : ")
            f.write(' / '.join([f"{k}: {v}" for k, v in rgb_values.items()]))
            f.write('\n')
    else:
        print('No match found.')
    # Load image in HSV
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(image)

    # Adjust HSV values
    h = np.clip(h.astype(np.int16)+ hsv_values["Hue"], 0, 179).astype(np.uint8)
    s = np.clip(s.astype(np.int16) + hsv_values["Saturation"], 0, 255).astype(np.uint8)
    v = np.clip(v.astype(np.int16) + hsv_values["Value"], 0, 255).astype(np.uint8)

    # Merge changes back to image
    adjusted_image = cv2.merge([h, s, v])
    
    # Return the adjusted image
    return cv2.cvtColor(adjusted_image, cv2.COLOR_HSV2BGR)

# Iterating over each image in the directory
for image_file in os.listdir('picture/'):
    image_path = os.path.join('picture/', image_file)
    
    # Apply changes
    adjusted_image = adjust_image(image_path)
    
    # Save to the result directory
    cv2.imwrite(os.path.join('picture_result/', image_file), adjusted_image)
    

