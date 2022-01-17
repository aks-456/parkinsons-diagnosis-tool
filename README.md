## Parkinson's Disease Diagnosis Tool using Vocal Features

Note: It is also possible to use the diagnosis tool with a classification model of your choice, as the tool is not dependent on the model. 

Parkinson's Disease (PD) affects Biomedical Voice Measurements (Vocal features) in patients. Affected vocal features include:

* MDVP:Fo(Hz) - Average vocal fundamental frequency 
* MDVP:Fhi(Hz) - Maximum vocal fundamental frequency 
* MDVP:Flo(Hz) - Minimum vocal fundamental frequency 
* MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP - Several measures of variation in fundamental frequency 
* MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA - Several measures of variation in amplitude 
* NHR,HNR - Two measures of ratio of noise to tonal components in the voice 
* RPDE,D2 - Two nonlinear dynamical complexity measures 
* DFA - Signal fractal scaling exponent 
* spread1,spread2,PPE - Three nonlinear measures of fundamental frequency variation 

In order to classify PD, the UCI ML Repository can be used for training and testing data: Parkinson's Disease Dataset, found here [https://archive.ics.uci.edu/ml/datasets/parkinsons]

A number of different approaches were used to classify the data, which was arranged in terms of patients with PD and patients without PD, as well as their vocal features from the dataset. The data was separated into a 80-20 train-test split, and recieved the following accuracies for each approach:

* Decision Tree Classifier - 89.4 % 
* K-nearest Neighbour - 83.2 % 
* Random Forest Classifier (RFC) - 94.9 % 
* Bagging Classifier - 89.9 % 
* Gradient Boosting - 89.8 % 

The most accurate one being the RFC model, with an accuracy of 94.9 % as mentioned above. More specifically, of the 59 sets of data used for testing, the RFC model accurately predicted 56. Note that the accuracy changes per each classification, but the model with 94.9% accuracy is labelled: 'model.sav'. A new model can be created by running: 'Model/PD Analysis RFC Model.ipynb'. Note that before doing so, it is necessary to run 'Model/Data/PD Analysis Data.ipynb' to create a readible set of data. 

## Frontend

The diagnosis tool is to perform a diagnosis of PD. It records the user's "sustained pronounciation" of the vowel a, (which according to: 'Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection', Little MA, McSharry PE, Roberts SJ, Costello DAE, Moroz IM. BioMedical Engineering OnLine 2007, 6:23 (26 June 2007) is the most effective in obtaining vocal features for PD Diagnosis). The UI is written in html and is a modified version of a wav file recorder made by [octavn](https://github.com/octavn) and can be found here: https://github.com/addpipe/simple-recorderjs-demo. The frontend code can be found to in the folder labelled: "diagnosis_tool/frontend". 
Note: The wav file recorder only works on **Chrome** and **Firefox** browsers.

## Backend

This is responsible for the extraction of vocal features from the voice recording, and connecting the 'frontend' to the classification model. There is a flask server which extracts vocal features from the recording using the 'Parselmouth' Python Library which can be found here: https://parselmouth.readthedocs.io/en/stable/. The parselmouth library is used to port Praat, a software for voice analytics, into python. With this package, vocal features such as Fo(Hz), Fli(Hz), Jitter(Abs) etc. for each recording and feed them to the classification model. This produces an output and displays either a 1, indicating the user has Parkinson's disease, or a 0, indicating the user does not. The backend is in the folder: "diagnosis_tool/backend". 

In addition to the flask server pyrebase was used to store and retrieve the audio recordings. The frontend sends the audio recording to firebase, and the backend flask server retrieves it each time a user has recorded their voice. The only change required to make is the Firebase database credentials which are unique for each application/developer, which must be replaced where indicated, in "diagnosis_tool/backend/main.py" and "diagnosis_tool/frontend/index.html". 
