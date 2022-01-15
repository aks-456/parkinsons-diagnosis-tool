## Parkinson's Diseases Diagnosis From Vocal Features

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

I used a number of different approaches to classify the data, which was arranged in terms of patients with PD and patients without PD, as well as their respective vocal features extracted from voice recordings. I separated the data into a 80-20 train-test split, and recieved the following accuracies for each approach:

* Decision Tree Classifier - 89.4 % 
* K-nearest Neighbour - 83.2 % 
* Random Forest Classifier (RFC) - 94.9 % 
* Bagging Classifier - 89.9 % 
* Gradient Boosting - 89.8 % 

The most accurate one being the RFC model, with an accuracy of 94.9 % as mentioned above. More specifically, of the 59 sets of data used for testing, the RFC model accurately predicted 56. Note that the accuracy changes per each classification, but the model with 94.9% accuracy is labelled: 'model.sav'. A new model can be created by running: 'Model/PD Analysis RFC Model.ipynb'. Note that before doing so, it is necessary to run 'Model/Data/PD Analysis Data.ipynb' to create a readible set of data. 

## Frontend

Along with the model, I implemented a user interface to perform a diagnosis. It records the user's sustained pronounciation of the vowel a, (which according to: 'Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection', Little MA, McSharry PE, Roberts SJ, Costello DAE, Moroz IM. BioMedical Engineering OnLine 2007, 6:23 (26 June 2007) is the most effective in obtaining vocal features for PD Diagnosis). The UI is written in html and I modified an existing version of a wav file recorder, which belongs to [octavn](https://github.com/octavn) and can be found here: https://github.com/addpipe/simple-recorderjs-demo. The frontend code can be found to in the folder labelled: "frontend". 
Note: The wav file recorder only works on **Chrome** and **Firefox** browsers.

## Backend

The frontent provides a basic user experience and it is accompanied with backend code, found in the "backend" folder. In the backend, I redirect the html frontend to a flask server which extracts vocal features from the recording. The vocal feature extraction is carried out through the Parselmouth Python library, which can be found here: https://parselmouth.readthedocs.io/en/stable/. The parselmouth library is used to port Praat, a software for voice analytics, into python. With this package, I extract vocal features for each recording and feed them into the ML model (model.sav). This produces an output and displays either a 1, indicating the user has Parkinson's disease, or a 0, indicating the user does not. This is contained in the file: "backend/main.py". 

In addition to the flask server I also use pyrebase to store and retrieve the audio recording of the patient. The frontend sends the audio recording to firebase, and the backend flask server retrieves it each time a user has recorded their voice. Currently I only expect there to be one recording at a time, and therefore did not bother to add a feature to change the name of the recording each time a user uploads one. The only change required to make is the Firebase database credentials which are unique for each application/developer, which must be replaced where indicated, in "backend/main.py" and "frontend/index.html". 
