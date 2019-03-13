# Senior Design Project
___
## Semi-Autonomous Car

Senior Design Team Repo
This is the Senior Design Team, DSCubed. We focus on creating a Semi autonomous vehicle.
Provided below is python code for creating a steering model, object recognition model,
and (Raspberry Pi vehicle 2 Computer Station server).

There are three sections. Steering Model, Image Classification Model, and Raspberry Pi TCP Server.


## Quick Start
Run the command command_central with optional arguments -sip, -vp, -sp, which configures the server interal ip, the video port on the server, and the sensor port on the server. Configure for your respective network. Ensure that the picamera is configured beforehand.


Server Side (Your PC) run
```bash
python command_central.py -sip '192.168.0.13' -vp '8006' -sp '8005'
```

Client Side (raspberry Pi) run

```bash
python client.py -sip '192.168.0.13' -vp '8006' -sp '8005'
```
Ensure that the port numbers match on both the client and the server.

## Steering Model

The steering model is based on [Nvidia's model](https://devblogs.nvidia.com/deep-learning-self-driving-cars/) which explains the architecture of their design. This model was implemented using Keras. The steering model is not implemented into the car as of the moment, but the training data and Keras code are available for training and implementation on your own version of the control system for the vehicle.

### Gathering Training Data

To create the data we used [Udacity's Car Simulator](https://github.com/udacity/self-driving-car-sim) to extract images and the corresponding steering metrics.

### Training Model

To train the model you must provide the path to the directory of folders that contain the data. The naming convention of the folders that contain the data must contain the string "Training Data". The path to the training parameters must also be specified. Change the values in the training_parameters.csv file to customize the variables in the steering model.

```bash
python train_steer.py -dd <data_dir> --tp <train_param>
```

To train the model on the default configuration settings with 6,600 images on

Computer Specification
Nvidia GTX 1080ti

took hours.

## Object recognition
The object recongition uses Haar Cascade Models, for both stoplights and stopsigns. Uses detectMultiscale function to find features from the models.

## Raspberry Pi TCP Server

The TCP server is loaded onto a Raspberry to communicate to the control center(PC) to the RC Vehicle. The server will stream visual data to the computer, the computer will then send control signals back to the vehicle. The control signals are sent over bluetooth communication that is built into the Raspberry Pi 3 B.
