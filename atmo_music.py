import os
import cv2
import requests
import numpy as np
import re
from matplotlib import pyplot as plt
import base64
import collections
import datetime
import fluidsynth
import glob
import pathlib
import pandas as pd
import pretty_midi
import seaborn as sns
import tensorflow as tf
from IPython import display
from typing import Optional

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
def make_keyword(image_path):
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
                    You are a curator of art galleries and exhibitions. Please select one atmosphere for each area and return it as a list whose name is "atmo".:

                    Light: "Bright", "Dark", "High Contrast"
                    Color: "Colorful", "Monochrome", "Warm", "Cool", "Neutral"
                    Texture: "Smooth", "Rough", "Soft", "Hard"
                    Time: "Day", "Night", "Dawn", "Morning"
                    Composition: "Simple", "Complex", "Balanced", "Unbalanced"
                    Mood: "Happy", "Sad", "Calm", "Chaotic"
                    Theme: "Urban", "Nature", "Abstract", "Portrait"

                    For example, atmo = ["Bright", "Warm", "Hard", "Soft", "Dawn", "Complex", "Happy", "Nature"]

                    Please also provide an explanation for each selected word in each area. Each area, type newline character:

                  Explanation:
                  For the Light area, "Bright" was chosen because the artwork has a cheerful and vibrant feel to it.

                  just return atmo list and explanation and the most strongly felt keyword like keyword="Happy"

                  Blow is output format
                  atmo = ["Bright", "Warm", "Hard", "Soft", "Dawn", "Complex", "Happy", "Nature"]
                  Explanation : For the Light area, "Bright" was chosen because the artwork has a cheerful and vibrant feel to it.
                  keyword = "Happy"
                  """

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
    

# 'choices' 키의 첫번째 요소 내부의 'message' 키의 'content' 값을 출력
    atmosphere = response.json()['choices'][0]['message']['content']
    Atmo = atmosphere.split('Explanation')[0]
    atmo = Atmo.split('atmo')[1]
    expl = atmosphere.split('Explanation')[1]
    explanation = expl.split('keyword')[0]
    keyword = atmosphere.split('keyword')[1]
    keyword = keyword[3:]
    print(Atmo)

    print(keyword)

#파일에 저장
    file = open("atmosphere.txt", "w")
    file.write("atmo")
    file.write(atmo)
    file.close()

    explanation = str(explanation)

    file = open("atmo_explanation","w")
    file.write("Explanation:\n")
    file.write(explanation)
    file.close()

    file = open("keyword.txt", "w")
    file.write(keyword)
    file.close()    # Return the adjusted image
    return keyword

# Iterating over each image in the directory
for image_file in os.listdir('picture_exhibition/'):
    image_path = os.path.join('picture_exhibition/', image_file)
    # Apply changes
    atmo_music = make_keyword(image_path)
    print(atmo_music)
    print("making keyword is finished")

  
