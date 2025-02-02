import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

from keras import Sequential
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore

time_step = 10
model = load_model('lstm_model.keras')

# Load data
data = pd.read_csv('dataset_lstm.csv')
data['DATE'] = pd.to_datetime(data['DATE'])
data.set_index('DATE', inplace=True)

# Preprocess data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data.values)

prediction_date = datetime(2025,3,15)

new_data = np.array([[data, 'tmax', 'tmin', 'precip', 'snow', 'wind']])
scaled_new_data = scaler.transform(new_data)
X_new = scaled_new_data.reshape((1, time_step, scaled_new_data.shape[1]))

# Predict
predicted_weather = model.predict(X_new)
predicted_weather = scaler.inverse_transform(predicted_weather)
print(f'Predicted Weather: {predicted_weather}')