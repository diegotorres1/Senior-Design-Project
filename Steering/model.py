# Author : Diego Torres
# Date of Modification : 3/5/2019
# Description : Create the model

###############################################################################
# Libraries Start
import pandas as pd
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Lambda, Conv2D, Dropout, MaxPooling2D, Dense, Flatten
# Libraries End
###############################################################################
class model():
    def __init__(self):
        print('-model created')

    def create_model(self, config_df):

        model = Sequential()
        # model.add(Lambda(lambda x : (x/127.5) - 1.0,input_shape = (int(config_df['image_height'][0]),int(config_df['image_width'][0]),int(config_df['image_channels'][0]))))
        input_shape = (int(config_df['image_height'][0]),int(config_df['image_width'][0]),int(config_df['image_channels'][0]))
        # convolution increase number of filters
        model.add(Conv2D(filters = 24, kernel_size = 5, strides = (2,2), activation = 'elu',input_shape=input_shape))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        # model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(filters = 36, kernel_size = 5, strides = (2,2), activation = 'elu'))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        # model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(filters = 48, kernel_size = 5, strides = (2,2), activation = 'elu'))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        # model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(filters = 64, kernel_size = 5, strides = (2,2), activation = 'elu'))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        # model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(filters = 64, kernel_size = 5, strides = (2,2), activation = 'elu'))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        model.add(MaxPooling2D(pool_size=(2, 2)))


        model.add(Flatten())


        model.add(Dense(100,activation = 'elu'))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        model.add(Dense(50,activation = 'elu'))
        model.add(Dropout(float(config_df['drop_probability'][0])))
        model.add(Dense(10,activation = 'elu'))
        model.add(Dense(1))

        return model
