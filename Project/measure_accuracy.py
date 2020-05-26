#!/usr/bin/python3 

import warnings
warnings.filterwarnings("ignore")
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

# Provide path to your test dataset
test_dir = "datasets/dogsVScats/test/"

# Preprocessing data
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(test_dir, target_size=(64,64),class_mode="binary",batch_size=32,shuffle=False)

model = load_model("dogVScat.h5") # Loading model
_, accuracy = model.evaluate_generator(test_generator, 2000/32) # Evaluating Accuracy

# Writing accuracy to accuracy.txt
file_obj = open("accuracy.txt", "w")
file_obj.write(f"{accuracy*100}")
file_obj.close()
