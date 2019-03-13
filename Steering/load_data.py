# Author : Diego Torres
# Date of Modification : 3/5/2019
# Description : Organize information for the training stage

###############################################################################
# Libraries Start
import pandas as pd
import cv2
import os
import matplotlib.image as mpimg
import numpy as np
from sklearn.model_selection import train_test_split
# Libraries End
###############################################################################
class load_data():
    def __init__(self,config_df):
        self.IMAGE_WIDTH = int(config_df['image_width'][0])
        self.IMAGE_HEIGHT = int(config_df['image_height'][0])
        self.IMAGE_CHANNELS = int(config_df['image_channels'][0])

        print('-load_data created')


    ############################################################################
    # Augmentation Start

    # get images
    def load_image(self, image_file):
        return mpimg.imread(image_file.strip())

    # format for the input of the model
    def preprocess(self,image):
        image = image[60:-25, :, :]
        image =cv2.resize(image, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
        return image

    # choose from left, center and right images
    def choose_image(self,center, left, right, steering_angle):
        choice = np.random.choice(3)
        if choice == 0:
            return self.load_image(left), steering_angle + 0.2
        elif choice == 1:
            return self.load_image(right), steering_angle - 0.2
        return self.load_image(center), steering_angle

    # flip image
    def random_flip(self, image, steering_angle):
        if np.random.rand() < 0.5:
            image = cv2.flip(image, 1)
            steering_angle = -steering_angle
        return image, steering_angle

    # translate image
    def random_translate(self,image, steering_angle, range_x, range_y):
        trans_x = range_x * (np.random.rand() - 0.5)
        trans_y = range_y * (np.random.rand() - 0.5)
        steering_angle += trans_x * 0.002
        trans_m = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
        height, width = image.shape[:2]
        image = cv2.warpAffine(image, trans_m, (width, height))
        return image, steering_angle

    # random shadows
    def random_shadow(self,image):
        # (x1, y1) and (x2, y2) forms a line
        # xm, ym gives all the locations of the image
        x1, y1 = self.IMAGE_WIDTH * np.random.rand(), 0
        x2, y2 = self.IMAGE_WIDTH * np.random.rand(), self.IMAGE_HEIGHT
        xm, ym = np.mgrid[0:self.IMAGE_HEIGHT, 0:self.IMAGE_WIDTH]

        # mathematically speaking, we want to set 1 below the line and zero otherwise
        # Our coordinate is up side down.  So, the above the line:
        # (ym-y1)/(xm-x1) > (y2-y1)/(x2-x1)
        # as x2 == x1 causes zero-division problem, we'll write it in the below form:
        # (ym-y1)*(x2-x1) - (y2-y1)*(xm-x1) > 0
        mask = np.zeros_like(image[:, :, 1])
        mask[(ym - y1) * (x2 - x1) - (y2 - y1) * (xm - x1) > 0] = 1

        # choose which side should have shadow and adjust saturation
        cond = mask == np.random.randint(2)
        s_ratio = np.random.uniform(low=0.2, high=0.5)

        # adjust Saturation in HLS(Hue, Light, Saturation)
        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        hls[:, :, 1][cond] = hls[:, :, 1][cond] * s_ratio
        return cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)

    # brighten/dim image
    def random_brightness(self,image):
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        ratio = 1.0 + 0.4 * (np.random.rand() - 0.5)
        hsv[:,:,2] =  hsv[:,:,2] * ratio
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    # augment
    def augment(self, center, left, right, steering_angle, range_x=100, range_y=10):
        image, steering_angle = self.choose_image(center, left, right, steering_angle)
        image, steering_angle = self.random_flip(image, steering_angle)
        image, steering_angle = self.random_translate(image, steering_angle, range_x, range_y)
        image = self.random_shadow(image)
        image = self.random_brightness(image)
        return image, steering_angle


    # Augmentation End
    ############################################################################

    # Generate training image give image paths and associated steering angles
    def batch_generator(self,image_paths, steering_angles, batch_size, is_training):
        images = np.empty([batch_size, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, self.IMAGE_CHANNELS])
        steers = np.empty(batch_size)

        while True:
            i = 0
            for index in np.random.permutation(image_paths.shape[0]):
                center, left, right = image_paths[index]
                steering_angle = steering_angles[index]
                # argumentation
                if is_training and np.random.rand() < 0.6:
                    image, steering_angle = self.augment( center, left, right, steering_angle)
                else:
                    image = self.load_image(center)
                # add the image and steering angle to the batch
                images[i] = self.preprocess(image)
                steers[i] = steering_angle
                i += 1
                if i == batch_size:
                    break
            yield images, steers


    # Generate training image give image paths and associated steering angles
    def predict_generator(self,image_paths, batch_size, is_training):
        images = np.empty([batch_size, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, self.IMAGE_CHANNELS])

        while True:
            i = 0
            for index in np.random.permutation(image_paths.shape[0]):
                center, left, right = image_paths[index]
                # argumentation
                if is_training and np.random.rand() < 0.6:
                    image, steering = self.choose_image(center, left, right, 0)
                else:
                    image = self.load_image(center)
                # add the image and steering angle to the batch
                images[i] = self.preprocess(image)
                i += 1
                if i == batch_size:
                    break
            yield images

    # load_data recieve path to csv containing training data
    def load_data_sample(self, path, name_list,config_df):
        test_size = float(config_df['test_size'][0])
        df = pd.read_csv(path, names = name_list,engine='python')
        print(list(df.columns.values))
        input = df[['center','left','right']].values
        output = df[['steering']].values


        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=, random_state=)
        # random_state = int for random seed for splitting
        # test_size = proportion of data set to include in the test
        input_train, input_test, output_train, output_test = train_test_split(input, output,test_size = test_size,random_state = 1)
        return [input_train, input_test, output_train, output_test]
