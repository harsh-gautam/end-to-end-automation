#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")
from keras.models import load_model

# Provide your model path
model_path = "dogVScat.h5"
model = load_model(model_path) # Loading the model

import json
import os.path

# Generating JSON data for model architecture based on iteration
json_path = "data.json"
if os.path.isfile(json_path):
    with open(json_path, "r+") as w:
        json_data = json.load(w)
        w.seek(0)
        w.write("")
        json_data["iteration"] += 1
        
        json_data_new = {}
        json_data_new["iteration"] = json_data["iteration"]
        json_data_new["layers"] = json_data["layers"]
        for layer in model.layers:
            json_data_new["layers"][layer.__class__.__name__] = 0
        for layer in model.layers:
            if layer.__class__.__name__:
                json_data_new["layers"][layer.__class__.__name__] += 1
        print(json_data_new)
        json.dump(json_data_new, w)
            
else:
    json_data = {"iteration":0,"layers":{}}
    for layer in model.layers:
        json_data["layers"][layer.__class__.__name__] = 0
    for layer in model.layers:
        if layer.__class__.__name__:
            json_data["layers"][layer.__class__.__name__] += 1
    print(json_data)
    with open(json_path, "w") as w:
        json.dump(json_data, w)


# Provide your python file path
filename = "run.py"

# Funtion to create new Convolution layer and return it
def conv_layer(filters, kernel_size, pool_size):
    conv = f"Conv2D(filters={filters}, kernel_size={kernel_size}, activation='relu')"
    maxpool = f"MaxPool2D(pool_size={pool_size})"
    return f"model.add({conv})\nmodel.add({maxpool})\n"

# Function to create new Fully Connected layer and return it
def dense_layer(neurons):
    dense = f"Dense(units={neurons}, activation='relu')"
    dropout = f"Dropout(0.5)"
    return f"model.add({dense})\nmodel.add({dropout})\n"

# Reading data from main file
with open(filename, "r") as f:
    data = f.readlines()

# Function to add new layers
def append_data(layer):
    index = [i for i, d in enumerate(data) if layer in d][-1]
    if "MaxPool" in layer:
        data.insert(index+1, conv_layer(filters, kernel_size, pool_size))
    elif "Dropout" in layer or "Dense" in layer:
        data.insert(index+1, dense_layer(neurons))

neurons = 256
filters = 64
kernel_size = (3, 3)
pool_size = (2, 2)

# Based on iterations tweaking the CNN architecture
with open(json_path, 'r') as f:
    json_data = json.load(f)
    
if json_data["iteration"] == 0:
    append_data("MaxPool2D")
    append_data("Dropout")
elif json_data["iteration"] == 1:
    filters = 128
    neurons = 128
    append_data("MaxPool2D")
    append_data("Dropout")
    
elif json_data["iteration"] == 2:
    filters = 128
    neurons = 64
    append_data("MaxPool2D")
    append_data("Dropout")
else:
    append_data("MaxPool2D")
    append_data("Dropout")

# Writing new data to the file
with open(filename, "w") as f:
    f.write("".join(data))

