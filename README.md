# Automatic Detection of Depression using Speech and Facial Recognition

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
