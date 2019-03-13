#Author : Diego Torres
# Date of Modification : 3/6/19
# Description : Test the weights generated
################################################################################
# Libaries Start

from train_model import train_model
from load_data import load_data
import cv2
from model import model
# from GPU_Checker import GPU_Checker
import pandas as pd # data analysis toolkit - create, read, update, delete datasets
import numpy as np #matrix math
from sklearn.model_selection import train_test_split #to split out training and testing data
#keras is a high level wrapper on top of tensorflow (machine learning library)
#The Sequential container is a linear stack of layers
from keras.models import Sequential
#popular optimization strategy that uses gradient descent
from keras.optimizers import Adam
#to save our model periodically as checkpoints for loading later
from keras.callbacks import ModelCheckpoint
#what types of layers do we want our model to have?
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
#helper class to define input shape and generate training images given image paths & steering angles
# from utils import INPUT_SHAPE, batch_generator
#for command line arguments
import argparse
#for reading files
import os
import sys

# Libaries End
################################################################################
def main():
    # Arguments
    parser = argparse.ArgumentParser(description = 'Process Training Params')
    parser.add_argument('-tp', help='training parameters',dest='param_dir',type=str, default='D:\\UCI\\Senior Design Project\\DSCubed V_2\\Steering\\training_parameters.csv')
    parser.add_argument('-ip', help='image',dest='image_path',type=str,default='')
    parser.add_argument('-wp', help='weights_path',dest='weights_path',type=str,default='D:\\UCI\\Senior Design Project\\checkpoints_4\\model-2336.h5')
    parser.add_argument('-dd', help='data directory',dest='data_dir',type=str,default='D:\\UCI\\Senior Design Project\\simulator-windows-64\\driving_log.csv')

    args = parser.parse_args()

    # Print Inputs Given
    print('=' * 10)
    print('Arguments: ')
    for key, value in vars(args).items():
        print('%s :\t%s' % (str(key), str(value)))
    print('=' * 10 + '\n')

    # Training Configuration File Load
    config_df = pd.read_csv(args.param_dir, encoding = 'utf-8')
    print('=' * 10)
    print('Configuration Settings')
    print((config_df.T).to_string())
    print('=' * 10)

    ###########################################################################
    # Load Data Start

    ld = load_data(config_df)
    name_list=['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
    print('\nLoad Data from ...')
    print(args.data_dir)
    data = ld.load_data_sample(args.data_dir, name_list,config_df)
    print(len(data[0]))
    # sys.exit(0)
    # Load Data End
    ###########################################################################

    m = model()

    model_h = m.create_model(config_df)
    model_h.load_weights(args.weights_path)
    model_h.compile(loss = 'mean_squared_error', optimizer = Adam(lr = float(config_df['learning_rate'][0])))

    #estimate accuracy on the data set
    x = data[0][40:41]
    y = data[2][40:41]

    print(x)
    print(y)
    # sys.exit()
    print('Evaluate')
    scores = model_h.evaluate_generator(\
        generator = ld.batch_generator(x, y, int(config_df['batch_size'][0]), False),\
        steps = 1,\
        verbose = True)

    print(model_h.metrics_names)
    print(scores)

    print('Predict : ')
    predictions = model_h.predict_generator(\
        generator = ld.predict_generator(x, 2, False),\
        steps = 1,\
        verbose = True)

    print(len(predictions))
    for item in predictions:
        print(item)
    print(y)
    # print(y)


def test_image():
    # Arguments
    parser = argparse.ArgumentParser(description = 'Process Training Params')
    parser.add_argument('-tp', help='training parameters',dest='param_dir',type=str, default='D:\\UCI\\Senior Design Project\\DSCubed V_2\\Steering\\training_parameters.csv')
    parser.add_argument('-ip', help='image',dest='image_path',type=str,default='')
    parser.add_argument('-wp', help='weights_path',dest='weights_path',type=str,default='D:\\UCI\\Senior Design Project\\checkpoints_4\\model-2336.h5')
    parser.add_argument('-dd', help='data directory',dest='data_dir',type=str,default='D:\\UCI\\Senior Design Project\\simulator-windows-64\\driving_log.csv')

    args = parser.parse_args()

    # Print Inputs Given
    print('=' * 10)
    print('Arguments: ')
    for key, value in vars(args).items():
        print('%s :\t%s' % (str(key), str(value)))
    print('=' * 10 + '\n')

    # Training Configuration File Load
    config_df = pd.read_csv(args.param_dir, encoding = 'utf-8')
    print('=' * 10)
    print('Configuration Settings')
    print((config_df.T).to_string())
    print('=' * 10)

    ###########################################################################
    # Load Data Start

    ld = load_data(config_df)
    name_list=['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
    print('\nLoad Data from ...')
    print(args.data_dir)
    data = ld.load_data_sample(args.data_dir, name_list,config_df)
    print(len(data[0]))
    # sys.exit(0)
    # Load Data End
    ###########################################################################

    m = model()

    model_h = m.create_model(config_df)
    model_h.load_weights(args.weights_path)
    model_h.compile(loss = 'mean_squared_error', optimizer = Adam(lr = float(config_df['learning_rate'][0])))


    # the code to implement in the car code itself, loading images and placing the image into the predict function
    # in the training process the images are uploaded through the Matplotlib library
    # in the webserver code, they are using PIL to load the image for some reason
    # I just need to check the consistency between Matplotlib and Cv2 and might need to convert

    #matplot lib returns RGB
    #cv2 returns BGR
    # preprocess is important for the color space conversion and resizing
    path = 'D:\\UCI\\Senior Design Project\\simulator-windows-64\\IMG\\center_2019_03_07_23_51_36_259.jpg'
    image = ld.load_image(path)
    image = ld.preprocess(image)
    cv2.imshow('this', image)
    sys.exit()

    steering_angle = float(model.predict(transformed_image_array, batch_size=1))












if __name__ == '__main__':
    test_image()
    print('test_model')
