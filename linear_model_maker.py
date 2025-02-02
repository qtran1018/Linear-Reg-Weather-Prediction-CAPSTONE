import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
import open_save

def make_model():
    selected_file = open_save.open_file()
    data = pd.read_csv(selected_file)
    date_format = "%m/%d/%y"
    data['DATE'] = pd.to_datetime(data['DATE'], format=date_format)

    data['Year'] = data['DATE'].dt.year
    data['Month'] = data['DATE'].dt.month
    data['Day'] = data['DATE'].dt.day

    data = data.dropna()

    x = data[['Year','Month','Day','TMAX', 'TMIN', 'PRCP', 'SNOW', 'AWND']] 
    y = data[['NEXT_TMAX', 'NEXT_TMIN', 'NEXT_PRCP', 'NEXT_SNOW', 'NEXT_AWND']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Initialize the base model (Linear Regression)
    base_model = LinearRegression()

    # Wrap the base model with MultiOutputRegressor
    model = MultiOutputRegressor(base_model)

    # Fit the model to the training data
    model.fit(x_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(x_test)

    # Calculate the mean squared error (MSE) for each target
    mse_tmax = mean_squared_error(y_test['NEXT_TMAX'], y_pred[:, 0])
    mse_tmin = mean_squared_error(y_test['NEXT_TMIN'], y_pred[:, 1])
    mse_prcp = mean_squared_error(y_test['NEXT_PRCP'], y_pred[:, 2])
    mse_snow = mean_squared_error(y_test['NEXT_SNOW'], y_pred[:, 3])
    mse_awnd = mean_squared_error(y_test['NEXT_AWND'], y_pred[:, 4])

    # Display the results
    print('Mean Squared Error for max temp:', mse_tmax)
    print('Mean Squared Error for min temp:', mse_tmin)
    print('Mean Squared Error for precipitation:', mse_prcp)
    print('Mean Squared Error for snow:', mse_snow)
    print('Mean Squared Error for wind:', mse_awnd)
    return model
