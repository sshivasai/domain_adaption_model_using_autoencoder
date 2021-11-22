# -*- coding: utf-8 -*-
"""Domain_adaption_model.ipynb

Here, I have use just a single image for Prediction another image 
i.e one Man image to predict another man image
 
Simple working example for Domain Adaption using Autoencoders
"""

from matplotlib.pyplot import imshow
import numpy as np
import cv2
from keras.preprocessing.image import img_to_array
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Sequential
import os
 
SIZE=256
 
 
img_data=[]
path1 = 'elon images path'
files=os.listdir(path1)
for i in tqdm(files):
    img=cv2.imread(path1+'/'+i,1)   #Change 0 to 1 for color images
    img=cv2.resize(img,(SIZE, SIZE))
    img_data.append(img_to_array(img))
    
 
img2_data=[]
path2 = 'rock images path'
files=os.listdir(path2)
for i in tqdm(files):
    img=cv2.imread(path2+'/'+i,1)  #Change 0 to 1 for color images
    img=cv2.resize(img,(SIZE, SIZE))
    img2_data.append(img_to_array(img))
 
img_array = np.reshape(img_data, (len(img_data), SIZE, SIZE, 3))
img_array = img_array.astype('float32') / 255.
 
img_array2 = np.reshape(img2_data, (len(img2_data), SIZE, SIZE, 3))
img_array2 = img_array2.astype('float32') / 255."""
 
#rock image
 
img_data1=[]
 
img1=cv2.imread('/content/Rock.jpeg', 1)   #Change 0 to 1 for color images
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)#Changing BGR to RGB to show images in true colors
img1=cv2.resize(img1,(SIZE, SIZE))
img_data1.append(img_to_array(img1))
img_array1 = np.reshape(img_data1, (len(img_data1), SIZE, SIZE, 3))
img_array1 = img_array1.astype('float32') / 255.
 
#elon image
img_data2=[]
img2=cv2.imread('/content/Elon.jpeg', 1)   #Change 0 to 1 for color images
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)#Changing BGR to RGB to show images in true colors
img2=cv2.resize(img2,(SIZE, SIZE))
img_data2.append(img_to_array(img2))
img_array2 = np.reshape(img_data2, (len(img_data2), SIZE, SIZE, 3))
img_array2 = img_array2.astype('float32') / 255.
 
 
import time
start=time.time()
 
 
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(SIZE, SIZE, 3)))
model.add(MaxPooling2D((2, 2), padding='same'))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D((2, 2), padding='same'))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
 
 
model.add(MaxPooling2D((2, 2), padding='same'))
     
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(8, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(3, (3, 3), activation='relu', padding='same'))
 
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.summary()
 
import tensorflow as tf
callbacks = [tf.keras.callbacks.TensorBoard(log_dir='einstein_logs')]
 
 
model.fit(img_array2, img_array1,
        epochs=1000,
        shuffle=True,
        callbacks=callbacks)
 
finish=time.time()
print('total_time = ', finish-start)
 
model.save('domain_adaption_autoencoder.model')
 
print("Output")
pred = model.predict(img_array2)
