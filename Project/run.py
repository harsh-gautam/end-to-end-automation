#!/usr/bin/env python

import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
print(tf.__version__)

train_dir = "datasets/dogsVScats/train/"
validation_dir = "datasets/dogsVScats/validation/"

# Data augmentation and preprocessing
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

validate_datagen = ImageDataGenerator(rescale=1./255)

IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64
BATCH_SIZE = 32

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    class_mode='binary',
    batch_size=BATCH_SIZE)

validate_generator = validate_datagen.flow_from_directory(
    validation_dir,
    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
    class_mode='binary',
    batch_size=BATCH_SIZE)

# Creating model architecture
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout

model = Sequential()

# First Convolution Layer
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPool2D(pool_size=(2, 2)))

# Second Convolution Layer
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))

# Flattening layer
model.add(Flatten())

# Fully Connected Layers
model.add(Dense(units=512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=1, activation='sigmoid'))

model.summary()

# compiling the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

epochs = 5
steps_per_epochs = round(20000*(1.-0.1)/BATCH_SIZE)
validation_steps=round(5000*0.1/BATCH_SIZE)

# Creating callbacks
from keras.callbacks import EarlyStopping, ModelCheckpoint

checkpoint = ModelCheckpoint("dogVScat.h5",
                            monitor="val_loss",
                            mode="min",
                            save_best_only=True,
                            verbose=1)
earlystop = EarlyStopping(monitor="val_loss",
                         mode="min",
                         verbose=1,
                         patience=5,
                         restore_best_weights=True)

callbacks = [checkpoint, earlystop]

model.fit_generator(train_generator,
                              validation_data=validate_generator,
                              validation_steps=validation_steps,
                              epochs=epochs,
                              steps_per_epoch=steps_per_epochs, 
                              callbacks=callbacks)

