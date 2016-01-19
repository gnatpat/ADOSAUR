# Automatic Detection of Depression using Speech and Facial Recognition

## Installation

You must have the following installed on your machine:
* [Node.js](https://nodejs.org/en/download/) & npm (comes with Node.js)
* [pip - the python package manager](http://pip.readthedocs.org/en/stable/installing/)
* [openCV - python package for Computer Vision](http://docs.opencv.org/)
* [avconv - video and audio converter](https://libav.org/avconv.html)

Once you have cloned the directory, navigate to the project's root directory and run the following command:

> `$ ./install.sh`

This script will install all the required dependencies for the web application and needed python packages.

**Note:** A computer with a CUDA capable GPU compatible with Theano must be used to run the code and the web app -  we used the NVIDIA GEFORCE GTX TITAN X.

## Web App

#### Starting the app

In a terminal, navigate to the ADOSAUR/app/Backend directory and run the following command to start the server:
> `$ ./start.sh`

Alternatively, if you have grunt-cli installed globally on your machine, just run:
> `$ grunt run`

Then in a web browser, open the page at http://localhost:8080.

## Raw Data

The set of Raw Data (video and audio recordings) should be placed in a folder named `rawData/`, with three subfolders - `labels/`, `RawAudio/` and `RawVideo/`.

## Pickled networks

The pickled audio and video convolutional neural networks named `audioCNN13.pickle` and `videoCNN1.save` should be placed in the `cnn/` directory.

## Testing

To run the tests, simply navigate to the root directory of `ADOSAUR` and run the following command:

> `py.test -v`
