import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

from keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore

# Load data
data = pd.read_csv('dataset_lstm.csv')
data['DATE'] = pd.to_datetime(data['DATE'])
data.set_index('DATE', inplace=True)

# Select relevant columns
data = data[['tmax', 'tmin', 'precip', 'snow', 'wind']]

# # Plot the data-------------------------------------------------------------------------------
# data.plot(figsize=(10, 6), subplots=True, title='Weather Data Over Time')
# plt.show()

# Preprocess the data (scale)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data.values)

# Prepare training and test data
training_data_len = int(np.ceil(len(scaled_data) * 0.8))
train_data = scaled_data[0:int(training_data_len), :]
valid_data = scaled_data[training_data_len:, :]

# Create sequences for training
def create_dataset(dataset, look_back=1):
    X, y = [], []
    for i in range(len(dataset) - look_back - 1):
        X.append(dataset[i:(i + look_back)])
        y.append(dataset[i + look_back, 0])  # Predicting HighTemp as an example
    return np.array(X), np.array(y)

look_back = 60  # Number of previous time steps to use for prediction
X_train, y_train = create_dataset(train_data, look_back)
X_valid, y_valid = create_dataset(valid_data, look_back)

# Reshape the data to [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], X_train.shape[2]))
X_valid = np.reshape(X_valid, (X_valid.shape[0], X_valid.shape[1], X_valid.shape[2]))

#----------------

# Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=25))
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, batch_size=1, epochs=1)
model.save('lstm_model.keras')
#--------------------------------------------------------------------------------
# plt.figure(figsize=(10, 6))
# plt.plot(train['tmax'], label='Training Data')
# plt.plot(valid[['tmax', 'Predictions']])
# plt.title('Temperature Prediction')
# plt.xlabel('Date')
# plt.ylabel('High Temperature')
# plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
# plt.show()
