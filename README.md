# Automatic Detection of Depression using Speech and Facial Recognition

## Installation

You must have the following installed on your machine:
* [Node.js](https://nodejs.org/en/download/) & npm (comes with Node.js)
* [pip - the python package manager](http://pip.readthedocs.org/en/stable/installing/)
* [openSMILE](http://www.audeering.com/research/opensmile)

Once you have cloned the directory, navigate to the project's root directory and run the following command:

> `$ ./install.sh`

## Web App

#### Coding Style

We will be using the [jslint](http://www.jslint.com/) coding style so please ensure it is installed on your code editor.
For Atom, [follow these instructions](https://atom.io/packages/jslint)

#### Starting the app

In a terminal, navigate to the ADOSAUR/app/Backend directory and run the following command to start the server:
> `$ ./start.sh`

Alternatively, if you have grunt-cli installed globally on your machine, just run:
> `$ grunt run`

Then in a web browser, open the page at http://localhost:8080.


## Database

The depression database is structured as follows in the `database/` folder:

* `audio/` contains the extracted features from the raw audio files
* `labels/` contains the labels for this data

Those 3 folders contains subfolders as the data is split into 3 sets:

* `Training/` for the training data set
* `Development/` for the development data set
* `Testing/` for the testing data set

The `audio` folder contain subfolders for the two exercises all of the participants did:

* `Northwind/`  Participants read aloud an excerpt of the fable “Die Sonne und der Wind” (The North Wind and the Sun), spoken in the German language
* `Freeform/` Participants respond to one of a number of questions such as: “What is your favourite dish?”; “What was your best gift, and why?”; “Discuss a sad childhood memory”, again in the German language

So we have 150 participants along with 150 labels, each of them performing the two exercises mentioned before,  so 300 data samples.
