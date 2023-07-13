from flask import Flask,request,send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flasgger import Swagger
import tensorflow as tf
from PIL import Image
import os

app=Flask(__name__) # it's a common step to start with this
Swagger(app) # pass the App to Swagger

current_directory = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(current_directory, "model")

classifier=tf.keras.models.load_model(model_path)

@app.route('/') # must be written to define the root page or main page to display
# this will display a web page having welcome all in it
def welcome():
    return "Welcome All"

# a page for predicting one sample, can be used through Postman
@app.route('/predict',methods=["POST"]) # by default it's GET method because we will pass our features as parameters
def predict_A_sample():
    """
    Let's landmark faces
    ---
    parameters:
        
        - name: image
          in: formData
          type: file
          required: true
    produces:
        - image/*
    responses:
        200:
            description: ok
            content:
                image/png: {}

    """
    image_path = os.path.join(current_directory, "image.png")
    if os.path.exists(image_path):
        # Delete the file
        os.remove(image_path)
    image=request.files.get("image")

    image = Image.open(image)
    image = image.convert('L')
    image = np.array(image.resize((96, 96)))
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    image = image.reshape((1, 96, 96,1))

    prediction=classifier.predict(image)[0]
    ax.scatter(prediction[0::2], prediction[1::2], c='red', marker='o')
    image_path = os.path.join(current_directory, "image.png")
    fig.savefig(image_path, bbox_inches='tight')

    image = open(image_path, 'rb')
    return  send_file(image, mimetype='image/png')

# a page for predicting csv file, can be used through Postman
@app.route('/predict_file',methods=["POST"])
def predict_A_File():

    """
    Let's landmark faces
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    
    responses:
        200:
            description: The output values
    """
    df_test=pd.read_csv(request.files.get("file")) 
    test_data=np.array(df_test)
    test_data=test_data.reshape(test_data.shape[0],96,96,1)
    prediction=classifier.predict(test_data)
    return "The digits are: " + str(list(prediction))



if __name__=='__main__':
    app.run()