#pip install azure-cognitiveservices-vision-face

import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont

def classify_image(img):
  API_KEY = 'f3a3382e22624ddda7c9dbcc0ae6fd81'
  ENDPOINT = 'https://engiefacerecognition.cognitiveservices.azure.com/'
  face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
  #img.show()
  image=Image.fromarray(img,"RGB")
  #print(image)
  image.save('test.jpg')
  #image.show()
  img_file = open('test.jpg', 'rb')
  #img_file=image
  # in below function image=img_file previously
  response_detection = face_client.face.detect_with_stream(
      image=img_file,
      detection_model='detection_01',
      recognition_model='recognition_04',
      return_face_attributes=['age', 'emotion'],
      )
  img1 = Image.open(img_file) #(img_file)
  draw = ImageDraw.Draw(img1) #(img)
  font = ImageFont.truetype('roboto.ttf', 11)
  for face in response_detection:
    age = face.face_attributes.age
    emotion = face.face_attributes.emotion
    neutral = '{0:.0f}%'.format(emotion.neutral * 100)
    happiness = '{0:.0f}%'.format(emotion.happiness * 100)
    anger = '{0:.0f}%'.format(emotion.anger * 100)
    sandness = '{0:.0f}%'.format(emotion.sadness * 100)

    rect = face.face_rectangle
    left = rect.left
    top = rect.top
    right = rect.width + left
    bottom = rect.height + top
    draw.rectangle(((left, top), (right, bottom)), outline='green', width=5)

    draw.text((right + 4, top), 'Age: ' + str(int(age)), fill=(255, 0, 0, 255), font=font) #before fill=(255,255,255)
    draw.text((right + 4, top+35), 'Neutral: ' + neutral, fill=(255, 0, 0, 255), font=font)
    draw.text((right + 4, top+70), 'Happy: ' + happiness, fill=(255, 0, 0, 255), font=font)
    draw.text((right + 4, top+105), 'Sad: ' + sandness, fill=(255, 0, 0, 255), font=font)
    draw.text((right + 4, top+140), 'Angry: ' + anger, fill=(255, 0, 0, 255), font=font) #, font=font
 # img.show()
 # img.save('test.jpg')
  return img1

#pip install gradio

import gradio as gr
image = gr.inputs.Image(shape=(50,200))
gr.Interface(fn=classify_image, 
             inputs=gr.Image(shape=(224, 224)),
             outputs=gr.Image(shape=(224, 224))).launch(debug=True)
