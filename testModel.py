"""
#POTENTIAL NEURAL NETWORK TEST

import pandas as pd
from modelAlgo import determineHydrate, genXYSequences
from tensorflow.keras.models import load_model

def getHydrates(filename):
    # Load the model
    model = load_model('hydrate_detection.h5')

    # Replace with your desired data file
    newData = pd.read_csv(filename)
    print('FILLNA\n')
    df = newData.fillna(method='ffill').fillna(method='bfill')
    #print(df)

    # Convert 'Time' column to datetime, then extract useful features (e.g., hour, day, etc.)
    newData['Time'] = pd.to_datetime(newData['Time'], errors='coerce')  # Convert to datetime, coercing errors to NaT
    newData['hour'] = newData['Time'].dt.hour  # Extract hour as a feature
    newData['day'] = newData['Time'].dt.day   # Extract day as a feature
    newData['month'] = newData['Time'].dt.month  # Extract month as a feature
    newData['year'] = newData['Time'].dt.year  # Extract year as a feature

    # Drop the original 'Time' column, as it's no longer needed
    newData = newData.drop(columns=['Time'])

    # Handle missing values (NaN) by filling or dropping them
    newData = newData.fillna(method='ffill').fillna(method='bfill')

    # Loop through the rows to check for hydrate detection
    for i in range(1, len(newData)):
        hydrateStatus = determineHydrate(newData.iloc[i], newData.iloc[i - 1])
        if hydrateStatus == 1:
            print('HYDRATE DETECTED AT ROW', i, ':', newData.iloc[i])

    XYSequences = genXYSequences('Bold_744H-10_31-11_07.csv')
    X = XYSequences[0]

    # Make predictions using the model
    probs = model.predict(X)

    # Print the data and predictions
    print(newData)
    print(probs)

    #print(df)

    return probs

getHydrates('Bold_744H-10_31-11_07.csv')

"""

# tests new data against model to see if there are hydrates

import joblib
import pandas as pd

from modelAlgo import determineHydrate

def testHydrate(filename):
    model = joblib.load('hydrate_detection.joblib')
    hydrateList = []

    newData = pd.read_csv(filename)
    newData = newData.fillna(method='ffill').fillna(method='bfill')

    for i in range(0,len(newData)):
        hydrateStatus = determineHydrate(newData.iloc[i],newData.iloc[i-1])
        if hydrateStatus == 1:
            hydrateList.append(1)
        else:
            hydrateList.append(0)    
    return hydrateList