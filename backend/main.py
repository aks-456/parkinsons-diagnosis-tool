import parselmouth
from parselmouth.praat import call, run_file
import numpy as np
import pickle
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import requests
from requests.auth import HTTPBasicAuth
import pyrebase


app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        filename = request.form['filename']
        return redirect(url_for('predictionsParkinsons', filename = filename))
    else:
       return ("Something went wrong")
    
# get the data for the requested query
@app.route('/predictionsParkinsons/<filename>')
#Flask route function
def predictionsParkinsons(filename):

    #Config
    config = {
        # Add Firebase Database Credentials
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()


    path_on_cloud = "audio/" + filename
    path_local = filename
    
    storage.child(path_on_cloud).download(path_local)

    local_filename = path_local
    # Go through all the wave files in the folder and measure pitch

    wave_file = local_filename

    #Parselmouth Object
    sound = parselmouth.Sound(wave_file)

    #Extract vocal features from audio recording
    (meanF0, f0max, f0min, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(sound, 75, 500, "Hertz")

    a_var = meanF0
    b_var = f0max
    c_var = f0min
    d_var = localJitter
    e_var = localabsoluteJitter
    f_var = rapJitter
    g_var = ppq5Jitter
    h_var = ddpJitter
    i_var = localShimmer
    j_var = localdbShimmer
    k_var = apq3Shimmer
    l_var = aqpq5Shimmer
    m_var = apq11Shimmer
    n_var = ddaShimmer
    #NHR
    p_var = hnr


    final_values = [a_var, b_var, c_var, d_var, e_var, f_var, g_var, h_var, i_var, j_var, k_var, l_var, m_var, n_var, p_var]
    final_features = np.array(final_values)


    
    #Make Prediction and return keyword in json format 
    with open('ML_diagnosis_model.sav', 'rb') as file:    # Load from file
        model = pickle.load(file)

    predictions = model.predict([final_values])
    #data = {"keyword": predictions}
    #return jsonify(data)
    return str(predictions)

    
# Function to extract vocal features from voice recording
def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    minF0 = call(pitch, "Get minimum", 0, 0, "hertz", "Parabolic") # get min pitch
    maxF0 = call(pitch, "Get maximum", 0, 0, "hertz", "Parabolic")  # get max pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation... and so on
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return meanF0, maxF0, minF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer




if __name__ == "__main__":
        app.run(host='127.0.0.1',port=5000,debug=True)


