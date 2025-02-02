import joblib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta, date


# Load the trained model
model = joblib.load('testdump.pkl')

# Function to make predictions
def predict_weather(tmax, tmin, precip, snow, wind, year, month, day):
    new_data = pd.DataFrame({
        'Year': [year],        
        'Month': [month],        
        'Day': [day],
        'TMAX': [tmax], 
        'TMIN': [tmin], 
        'PRCP': [precip],
        'SNOW': [snow],
        'AWND': [wind]
    })
    predicted_values = model.predict(new_data)
    return predicted_values[0][0], predicted_values[0][1], predicted_values[0][2], predicted_values[0][3], predicted_values[0][4]


# GUI using Tkinter
def run_app():
    #Make the window
    root = Tk()
    root.title("Weather Predictor")
    tomorrow = datetime.now() + timedelta(days=1)
    
    #make a notebook
    notebook = ttk.Notebook(root) 
    notebook.grid(row=0, column=0, sticky='nsew')

    #make the tabs
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook) 
    #tab3 = ttk.Frame(notebook)

    #add tabs to the notebook
    notebook.add(tab1, text="Single-day")
    notebook.add(tab2, text="Multi-day")
    #notebook.add(tab3, text="Graph")

    #create the 1st grid-frame. This holds today's date
    frame_data = ttk.Frame(tab1, padding="10", relief="ridge") 
    frame_data.grid(row=0, column=0, padx=10, pady=5)

    #create the 2nd grid-frame. This holds the text inputs, predict-button, and results
    frame_data2 = ttk.Frame(tab1, padding="10", relief="ridge") 
    frame_data2.grid(row=1, column=0, padx=10, pady=5)

    date_label = ttk.Label(frame_data, text=f"Input data for today's date: {date.today()} or latest available.\nPredicting for tomorrow's values by default")
    date_label.grid(column=0, row=0, columnspan=2, padx=10, pady=5)

    #tomorrow_date_label = ttk.Label(frame_data2, text=f"Tomorrow's date: {date.today() + timedelta(days=1)}")
    #tomorrow_date_label.grid(column=0, row=1, columnspan=2, padx=10, pady=5)
                
    #Make the labels and textfields
    #Textfields are for TODAY's actual measurements
    ttk.Label(frame_data2, text="Temp High").grid(column=0, row=0, padx=10, pady=5)
    tmax_entry = ttk.Entry(frame_data2)
    tmax_entry.grid(column=1, row=0, padx=10, pady=5)

    ttk.Label(frame_data2, text="Temp Low").grid(column=0, row=1, padx=10, pady=5)
    tmin_entry = ttk.Entry(frame_data2)
    tmin_entry.grid(column=1, row=1, padx=10, pady=5)

    ttk.Label(frame_data2, text="Precip").grid(column=0, row=2, padx=10, pady=5)
    precip_entry = ttk.Entry(frame_data2)
    precip_entry.grid(column=1, row=2, padx=10, pady=5)

    ttk.Label(frame_data2, text="Snow").grid(column=0, row=3, padx=10, pady=5)
    snow_entry = ttk.Entry(frame_data2)
    snow_entry.grid(column=1, row=3, padx=10, pady=5)

    ttk.Label(frame_data2, text="Wind").grid(column=0, row=4, padx=10, pady=5)
    wind_entry = ttk.Entry(frame_data2)
    wind_entry.grid(column=1, row=4, padx=10, pady=6)

    #Pre-populates the fields for TOMORROW'S date -- the one being predicted
    #Can disable the textfields if not testing the model; forces it for next-day predictions only
    ttk.Label(frame_data2, text="Year").grid(column=0, row=5, padx=10, pady=5)
    year_entry = ttk.Entry(frame_data2)
    year_entry.insert(END,tomorrow.year)
    #year_entry.config(state=DISABLED)
    year_entry.grid(column=1, row=5, padx=10, pady=7)

    ttk.Label(frame_data2, text="Month").grid(column=0, row=6, padx=10, pady=5)
    month_entry = ttk.Entry(frame_data2)
    month_entry.insert(END,tomorrow.month)
    #month_entry.config(state=DISABLED)
    month_entry.grid(column=1, row=6, padx=10, pady=5)

    ttk.Label(frame_data2, text="Day").grid(column=0, row=7, padx=10, pady=5)
    day_entry = ttk.Entry(frame_data2)
    day_entry.insert(END,tomorrow.day)
    #day_entry.config(state=DISABLED)
    day_entry.grid(column=1, row=7, padx=10, pady=5)

    result_label = ttk.Label(frame_data2, text="Results")
    result_label.grid(column=0, row=9, columnspan=2, padx=10, pady=5)

    def on_predict():
        try:
            tmax = float(tmax_entry.get())
            tmin = float(tmin_entry.get())
            precip = float(precip_entry.get())
            snow = float(snow_entry.get())
            wind = float(wind_entry.get())
            year = int(year_entry.get())
            month = int(month_entry.get())
            day = int(day_entry.get())
            predicted_tmax, predicted_tmin, predicted_precip, predicted_snow, predicted_wind = predict_weather(tmax, tmin, precip, snow, wind, year, month, day)

            #Checks if precip snow or wind is less than 0. Set to 0 if true.
            if predicted_precip < 0:
                predicted_precip = 0
            if predicted_snow < 0:
                predicted_snow = 0
            if predicted_wind < 0:
                predicted_wind = 0

            result_label.config(text=f"Predicted Temp Max: {predicted_tmax:.2f}\nPredicted Temp Min: {predicted_tmin:.2f}\nPredicted Precip: {predicted_precip:.2f}\nPredicted Snow: {predicted_snow:.2f}\nPredicted Wind: {predicted_wind:.2f}")
        except:
            result_label.config(text='Error. Fill all fields and use numbers only.')

        #Checks if precip snow or wind is less than 0. Set to 0 if true.
        if predicted_precip < 0:
            predicted_precip = 0
        if predicted_snow < 0:
            predicted_snow = 0
        if predicted_wind < 0:
            predicted_wind = 0

    # Predict Button
    predict_button = ttk.Button(frame_data2, text="Predict", command=on_predict)
    predict_button.grid(column=0, row=8,columnspan=2, padx=2, pady=5)

#---------------------------------------------------------------------------------
    #2nd tab
    #create the 1st grid-frame. This holds today's date
    frame_data3 = ttk.Frame(tab2, padding="10", relief="ridge") 
    frame_data3.grid(row=0, column=0, padx=10, pady=5)

    #create the 2nd grid-frame. This holds the text inputs, predict-button, and results
    frame_data4 = ttk.Frame(tab2, padding="10", relief="ridge") 
    frame_data4.grid(row=1, column=0, padx=10, pady=5)

    date_label2 = ttk.Label(frame_data3, text=f"Input data for today's date: {date.today()}\nPredicting for tomorrow's values by default")
    date_label2.grid(column=0, row=0, columnspan=2, padx=10, pady=5)

    ttk.Label(frame_data4, text="Temp High").grid(column=0, row=0, padx=10, pady=5)
    tmax_entry2 = ttk.Entry(frame_data4)
    tmax_entry2.grid(column=1, row=0, padx=10, pady=5)

    ttk.Label(frame_data4, text="Temp Low").grid(column=0, row=1, padx=10, pady=5)
    tmin_entry2 = ttk.Entry(frame_data4)
    tmin_entry2.grid(column=1, row=1, padx=10, pady=5)

    ttk.Label(frame_data4, text="Precip").grid(column=0, row=2, padx=10, pady=5)
    precip_entry2 = ttk.Entry(frame_data4)
    precip_entry2.grid(column=1, row=2, padx=10, pady=5)

    ttk.Label(frame_data4, text="Snow").grid(column=0, row=3, padx=10, pady=5)
    snow_entry2 = ttk.Entry(frame_data4)
    snow_entry2.grid(column=1, row=3, padx=10, pady=5)

    ttk.Label(frame_data4, text="Wind").grid(column=0, row=4, padx=10, pady=5)
    wind_entry2 = ttk.Entry(frame_data4)
    wind_entry2.grid(column=1, row=4, padx=10, pady=6)

    #Pre-populates the fields for TOMORROW'S date -- the one being predicted
    #Can disable the textfields if not testing the model; forces it for next-day predictions only
    ttk.Label(frame_data4, text="Year").grid(column=0, row=5, padx=10, pady=5)
    year_entry2 = ttk.Entry(frame_data4)
    year_entry2.insert(END,tomorrow.year)
    #year_entry.config(state=DISABLED)
    year_entry2.grid(column=1, row=5, padx=10, pady=7)

    ttk.Label(frame_data4, text="Month").grid(column=0, row=6, padx=10, pady=5)
    month_entry2 = ttk.Entry(frame_data4)
    month_entry2.insert(END,tomorrow.month)
    #month_entry.config(state=DISABLED)
    month_entry2.grid(column=1, row=6, padx=10, pady=5)

    ttk.Label(frame_data4, text="Day").grid(column=0, row=7, padx=10, pady=5)
    day_entry2 = ttk.Entry(frame_data4)
    day_entry2.insert(END,tomorrow.day)
    #day_entry.config(state=DISABLED)
    day_entry2.grid(column=1, row=7, padx=10, pady=5)

    result_label2 = ttk.Label(frame_data4, text="Results")
    result_label2.grid(column=0, row=9, columnspan=2, padx=10, pady=5)

    def on_far_predict():
        try:
            dates = []
            temp_max = []
            temp_min = []
            tmax2 = float(tmax_entry2.get())
            tmin2 = float(tmin_entry2.get())
            precip2 = float(precip_entry2.get())
            snow2 = float(snow_entry2.get())
            wind2 = float(wind_entry2.get())
            year2 = int(year_entry2.get())
            month2 = int(month_entry2.get())
            day2 = int(day_entry2.get())

            #Predicted date starts as of now, increments by 1 through each iteration
            predicted_date2 = datetime.now()
            day_diff = (date(year2, month2, day2)-datetime.now().date()).days
            
            #if day_diff > 180:
            for i in range(day_diff):
                predicted_tmax2, predicted_tmin2, predicted_precip2, predicted_snow2, predicted_wind2 = predict_weather(tmax2, tmin2, precip2, snow2, wind2, year2, month2, day2)
                
                #Checks if precip snow or wind is less than 0. Set to 0 if true.
                if predicted_precip2 < 0:
                    predicted_precip2 = 0
                if predicted_snow2 < 0:
                    predicted_snow2 = 0
                if predicted_wind2 < 0:
                    predicted_wind2 = 0
                
                tmax2 = predicted_tmax2
                tmin2 = predicted_tmin2
                precip2 = predicted_precip2
                snow2 = predicted_snow2
                wind2 = predicted_wind2
                
                predicted_date2 += timedelta(days=1)
                year2 = predicted_date2.year
                month2 = predicted_date2.month
                day2 = predicted_date2.day
                print(f"Day {i}: {predicted_date2.date()}")

                dates.append(predicted_date2)
                temp_max.append(predicted_tmax2)
                temp_min.append(predicted_tmin2)

            plt.plot(dates, temp_max, marker='o', label="Max Temp")
            plt.plot(dates, temp_min, marker='o', color='g', label="Min Temp")
            plt.xlabel = "Dates"
            plt.ylabel = "Temperature"
            plt.legend()
            #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
            plt.xticks([dates[0], dates[-1]], rotation=45)
            plt.gcf().autofmt_xdate()
            plt.show()

            #else:
             #   result_label2.config(text=f"The search limit is 180 days out. You input {day_diff}")

            result_label2.config(text=f"Predicted Temp Max: {predicted_tmax2:.2f}\nPredicted Temp Min: {predicted_tmin2:.2f}\nPredicted Precip: {predicted_precip2:.2f}\nPredicted Snow: {predicted_snow2:.2f}\nPredicted Wind: {predicted_wind2:.2f}")
        except Exception as e:
            result_label2.config(text='Error. Fill all fields and use numbers only.')
            print(e)

    far_predict_button = ttk.Button(frame_data4, text="Far Predict", command=on_far_predict)
    far_predict_button.grid(column=0, row=8,columnspan=2, padx=2, pady=5)

    # Run the app loop
    root.mainloop()

if __name__ == "__main__":
    run_app()
