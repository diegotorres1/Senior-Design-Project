#Author: Diego Torres
#Date Modification : 10/20/2018
#Description : train_steer handles the calling the main processes for training
	#the steering. The main processes that it calls are
		#Loading the Data from the CSV files
		#Creating the model
		#Then training the model on the data that was loaded



################################################################################
# Libaries Start

from train_model import train_model
from load_data import load_data
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

    # Create helper objects
    ld = load_data(config_df)
    tm = train_model()
    cm = model()



    ###########################################################################
    # Load Data Start
    name_list=['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
    print('\nLoad Data from ...')
    print(args.data_dir)
    data = ld.load_data_sample(args.data_dir, name_list,config_df)
    # Load Data End
    ###########################################################################


    ###########################################################################
    # Create Model
    print('\nCreating the model ... ')
    model_h = cm.create_model(config_df)
    # Create Model End
    ###########################################################################


    ###########################################################################
    # Train Model Start
    print('\nBegin training the model ...')
    print(config_df['checkpoint_path'][0])
    tm.train(model_h,config_df,data)
    # Train Model End
    ###########################################################################





if __name__ == '__main__':
	main()
	print('Train Steering Complete')
	print('Libraries used :')
	print('\t--Keras')
	print('\t--Numpy')
	print('\t--Pandas')
