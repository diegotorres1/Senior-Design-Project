# Author : Diego Torres
# Date of Modification : 3/5/2019
# Description : Training Stage

###############################################################################
# Libraries Start
import pandas as pd
import numpy as np
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint
from load_data import load_data
import math
# Libraries End
###############################################################################

class train_model():
    def __init__(self):
        print('-train_model created')

    def train(self, model,config_df,data):
        [input_train, input_test, output_train, output_test] = data
        # configure the learning process via compilation
        model.compile(loss = 'mean_squared_error', optimizer = Adam(lr = float(config_df['learning_rate'][0])))
        ld = load_data(config_df)

        # checkpoint
        checkpoint = ModelCheckpoint(\
            config_df['checkpoint_path'][0] +'model-{epoch:03d}.h5',\
            monitor = 'val_loss',\
            verbose = 1,\
            save_best_only = config_df['save_best_only'][0],\
            mode = 'auto'\
        )\

        #begin training
        model.fit_generator(\
            ld.batch_generator(input_train, output_train, int(config_df['batch_size'][0]), False),\
            steps_per_epoch = math.ceil(len(input_train) / int(config_df['batch_size'][0])),\
            epochs = int(config_df['epochs'][0]),\
            verbose = 1,\
            callbacks = [checkpoint],\
            validation_data = ld.batch_generator(input_test, output_test, int(config_df['batch_size'][0]), False),\
            validation_steps = math.ceil(len(input_test) / int(config_df['batch_size'][0])),\
            # validation_freq = 2,\
        )\
