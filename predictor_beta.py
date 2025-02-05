import joblib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
import numpy as np
#import matplotlib.dates as mdates
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta, date
import open_save
import export_model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
   
def run_app():

    def predict_weather(tmax, tmin, precip, snow, wind, year, month, day):
        model = joblib.load(choose_model_field.get())
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
    
    def on_predict_single():
        try:
            TMAX = float(tmax_entry.get())
            TMIN = float(tmin_entry.get())
            PRCP = float(precip_entry.get())
            SNOW = float(snow_entry.get())
            AWND = float(wind_entry.get())
            year = int(year_entry.get())
            month = int(month_entry.get())
            day = int(day_entry.get())
            predicted_tmax, predicted_tmin, predicted_precip, predicted_snow, predicted_wind = predict_weather(
                TMAX, TMIN, PRCP, SNOW, AWND, year, month, day)

            result_values.config(text=f"Predicted Temp Max: {predicted_tmax:.2f}\nPredicted Temp Min: {predicted_tmin:.2f}\nPredicted Precip: {predicted_precip:.2f}\nPredicted Snow: {predicted_snow:.2f}\nPredicted Wind: {predicted_wind:.2f}")
        except:
            result_values.config(text='Error. Fill all fields and use numbers only.')

    def on_predict_multi():
        try:
            #Clear the graph plot to prep for a new prediction
            plt.cla()

            #Arrays to hold data for plotting and
            dates = []
            max_temps = []
            min_temps = []

            #Get values from the text entry boxes
            TMAX = float(tmax_entry.get())
            TMIN = float(tmin_entry.get())
            PRCP = float(precip_entry.get())
            SNOW = float(snow_entry.get())
            AWND = float(wind_entry.get())
            year = int(year_entry.get())
            month = int(month_entry.get())
            day = int(day_entry.get())

            #Predicted date starts as of now, increments by 1 through each iteration
            predicted_date = datetime.now()
            day_diff = (date(year, month, day)-datetime.now().date()).days
            
            #Loop for the difference in days between the selected date and the current day (TODAY)
            #Feed the predicted data back into the model until the desired date is reached
            for i in range(day_diff):
                predicted_tmax, predicted_tmin, predicted_precip, predicted_snow, predicted_wind = predict_weather(TMAX, TMIN, PRCP, SNOW, AWND, year, month, day)
                TMAX = predicted_tmax
                TMIN = predicted_tmin
                PRCP = predicted_precip
                SNOW = predicted_snow
                AWND = predicted_wind
                
                predicted_date += timedelta(days=1)
                year = predicted_date.year
                month = predicted_date.month
                day = predicted_date.day
                #print(f"Day {i}: {predicted_date.date()}")

                dates.append(predicted_date)
                max_temps.append(predicted_tmax)
                min_temps.append(predicted_tmin)

            #Overwrite the results_values label to display the predictions
            result_values.config(text=f"Predicted Temp Max: {predicted_tmax:.2f}\nPredicted Temp Min: {predicted_tmin:.2f}\nPredicted Precip: {predicted_precip:.2f}\nPredicted Snow: {predicted_snow:.2f}\nPredicted Wind: {predicted_wind:.2f}")
            
            #Plot
            plt.plot(dates, max_temps, marker='o', label="Max Temp")
            plt.plot(dates, min_temps, marker='o', color='g', label="Min Temp")
            plt.xlabel("Dates")
            plt.ylabel("Temperature")
            plt.legend()
            #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
            plt.xticks([dates[0], dates[-1]], rotation=45)
            plt.gcf().autofmt_xdate()
            plt.show()

            # fig,ax = plt.subplots()
            # ax.plot(dates, max_temps, marker='o', label="Max Temp")
            # ax.plot(dates, min_temps, marker='o', color='g', label="Min Temp")
            # ax.set_xlabel('Dates')
            # ax.set_ylabel('Temperature')

        except Exception as e:
            result_values.config(text='Error. Fill all fields with valid values and use numbers only.')
            print(e)

    def choose_model():
        choose_model_field.delete(0,END)
        choose_model_field.insert(END,open_save.open_file_model())

    def graph_data():
        df = pd.read_csv(data_loc_field.get())
        # Convert the 'date' column to datetime objects
        df['DATE'] = pd.to_datetime(df['DATE'])

        #Get data for dates and temps
        dates = date2num(df['DATE'])  # Convert datetime objects to numerical format
        max_temps = df['TMAX']
        min_temps = df['TMIN']

        #Plot the values for TMAX
        plt.plot(df['DATE'], max_temps, label='Max Temperature Data')
        plt.plot(df['DATE'], min_temps, label='Min Temperature Data')

        #Regression lines
        slope_max, intercept_max = np.polyfit(dates, max_temps, 1)
        regression_line_max = slope_max * dates + intercept_max
        slope_min, intercept_min = np.polyfit(dates, min_temps, 1)
        regression_line_min = slope_min * dates + intercept_min

        regression_dates = num2date(dates)

        # Plot the regression
        plt.plot(regression_dates, regression_line_max, color='red', label='Max temp Regression Line')
        plt.plot(regression_dates, regression_line_min, color='blue', label='Min temp Regression Line')
        

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Temperature (°F)')
        plt.title('Temperature Data with Regression Line')
        plt.legend()
        plt.text(df['DATE'].iloc[1], regression_line_max[1], f'Slope: {slope_max:.2f}', color='red')
        plt.text(df['DATE'].iloc[1], regression_line_min[1], f'Slope: {slope_min:.2f}', color='blue')
        # Show the plot
        plt.show()
#------------------------------------------------------------------------------------------------
# region MAIN_WINDOW
    #Make the window
    root = Tk()
    root.title("Weather Predictor")
    
    #make a notebook
    notebook = ttk.Notebook(root) 
    notebook.grid(row=0, column=0, sticky='nsew')

    #make the tabs
    model_maker = ttk.Frame(notebook)
    
    #TODO:single_day 1/2. Should change the single day frame var but I don't want to touch it any further as of now. I THINK replace/rename all single_day would work.
    single_day = ttk.Frame(notebook) 
    # graph = ttk.Frame(notebook)

    #Add tabs to the notebook
    notebook.add(model_maker, text="Model Maker")
    
    #TODO:single_day 2/2. Should change the single day frame var but I don't want to touch it any further as of now.
    notebook.add(single_day, text="Predictor")
    # notebook.add(graph, text="Mutli-Day Graph")

    #Canvas
    # canvas = FigureCanvasTkAgg(fig,)
    # canvas.draw()
    # canvas.get_tk_widget().grid(row=0,column=0,padx=10,pady=5,sticky="nsew")
    # root.grid_rowconfigure(0, weight=1)
    # root.grid_columnconfigure(0, weight=1)
    # graph.grid_rowconfigure(0, weight=1)
    # graph.grid_columnconfigure(0, weight=1)    

# endregion MAIN_WINDOW
#------------------------------------------------------------------------------------------------
# region MODEL_MAKER
    #MODEL MAKER TAB
    #Top frame for info display purposes
    frame_header = ttk.Frame(model_maker,padding="10", relief="ridge")
    frame_header.grid(row=0,column=0,padx=10,pady=5)

    #Bottom frame to hold text fields and buttons for making the model
    frame_model_maker = ttk.Frame(model_maker, padding="10", relief="ridge") 
    frame_model_maker.grid(row=1, column=0, padx=10, pady=5)
#------------------------------------------------------------------------------------------------
    #Header info
    ttk.Label(
        frame_header,
        text='Select the save location\nSelect the dataset'
    ).grid(row=0,column=1,padx=10,pady=5)
#------------------------------------------------------------------------------------------------
    #Edit the text field for save location         
    def change_save_loc():
        save_loc_field.delete(0,END)
        save_loc_field.insert(END,open_save.save_file())
    #Edit the text field for where the dataset to be used is
    def change_file_loc():
        data_loc_field.delete(0,END)
        data_loc_field.insert(END,open_save.open_file_csv())
    #Creates the datasets. Location info --> Export Model.py --> Model Maker.py --> Export Model.py dump
    def create_model():
        try:
            save_spot = save_loc_field.get()
            data_spot = data_loc_field.get()
            export_model.export_model(save_spot,data_spot)
        except Exception as e:
            export_model.show_message(e)

#------------------------------------------------------------------------------------------------
    #Get location to save model to
    ttk.Label(frame_model_maker, text="Save model to:").grid(row=0,column=0,padx=10,pady=5)
    save_loc_field = ttk.Entry(frame_model_maker)
    save_loc_field.grid(row=0,column=1,padx=10,pady=5)

    save_loc_btn = ttk.Button(frame_model_maker, text="Select save location", command=change_save_loc)
    save_loc_btn.grid(row=0,column=2,padx=10,pady=5)

    #Get location of the dataset to use for model creation
    ttk.Label(frame_model_maker, text="Select dataset:").grid(row=1,column=0,padx=10,pady=5)
    data_loc_field = ttk.Entry(frame_model_maker)
    data_loc_field.grid(row=1,column=1,padx=10,pady=5)

    data_loc_btn = ttk.Button(frame_model_maker, text="Select dataset", command=change_file_loc)
    data_loc_btn.grid(row=1,column=2,padx=10,pady=5)
    
    plot_data_btn = ttk.Button(frame_model_maker, text="Graph data", command=graph_data)
    plot_data_btn.grid(row=1,column=3,padx=10,pady=5)

    #Create the model.
    create_model_btn = ttk.Button(frame_model_maker,text="Make the model", command=create_model)
    create_model_btn.grid(row=2,column=1,padx=10,pady=5)
# endregion MODEL_MAKER
#------------------------------------------------------------------------------------------------
# region SINGLE_DAY

    frame_instructions = ttk.Frame(single_day, padding="10",relief="solid")
    frame_instructions.grid(row=0,column=0,padx=10,pady=5)
    ttk.Label(frame_instructions, text="Step 1: Choose your model.\nStep 2: Input the latest weather data avaialble.\nStep 3: Input the desired predicted date. Set to tomorrow by default.\nNOTE: This is intended to predict the next day from the date of your input weather data.").grid(row=0,column=1,padx=10,pady=5)

    frame_data_fields = ttk.Frame(single_day,padding="10",relief="ridge")
    frame_data_fields.grid(row=1,column=0,padx=10,pady=5)

    ttk.Label(frame_data_fields, text="Choose model").grid(row=0,column=0,padx=10,pady=5)
    choose_model_field = ttk.Entry(frame_data_fields)
    choose_model_field.grid(row=0,column=1,padx=10,pady=5)
    choose_model_loc_btn = ttk.Button(frame_data_fields,text="Open", command=choose_model)
    choose_model_loc_btn.grid(row=0,column=2,padx=10,pady=5)

    tomorrow = datetime.now() + timedelta(days=1)

    #---------------------------------------------------------------------------------------------
    ttk.Label(frame_data_fields, text="Temp High (F)").grid(row=1, column=0, padx=10, pady=5)
    tmax_entry = ttk.Entry(frame_data_fields)
    tmax_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(frame_data_fields, text="Temp Low (F)").grid(row=2, column=0, padx=10, pady=5)
    tmin_entry = ttk.Entry(frame_data_fields)
    tmin_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(frame_data_fields, text="Precip (in.)").grid(row=3, column=0, padx=10, pady=5)
    precip_entry = ttk.Entry(frame_data_fields)
    precip_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(frame_data_fields, text="Snow (in.)").grid(row=4, column=0, padx=10, pady=5)
    snow_entry = ttk.Entry(frame_data_fields)
    snow_entry.grid(row=4, column=1, padx=10, pady=5)

    ttk.Label(frame_data_fields, text="Wind (MPH)").grid(row=5, column=0, padx=10, pady=5)
    wind_entry = ttk.Entry(frame_data_fields)
    wind_entry.grid(row=5, column=1, padx=10, pady=5)

    #Pre-populates the fields for TOMORROW'S date -- the one being predicted
    ttk.Label(frame_data_fields, text="Year").grid(column=0, row=6, padx=10, pady=5)
    year_entry = ttk.Entry(frame_data_fields)
    year_entry.insert(END,tomorrow.year)
    year_entry.grid(row=6, column=1, padx=10, pady=7)

    ttk.Label(frame_data_fields, text="Month").grid(column=0, row=7, padx=10, pady=5)
    month_entry = ttk.Entry(frame_data_fields)
    month_entry.insert(END,tomorrow.month)
    month_entry.grid(row=7, column=1, padx=10, pady=5)

    ttk.Label(frame_data_fields, text="Day").grid(column=0, row=8, padx=10, pady=5)
    day_entry = ttk.Entry(frame_data_fields)
    day_entry.insert(END,tomorrow.day)
    day_entry.grid(row=8, column=1, padx=10, pady=5)

    ttk.Button(frame_data_fields,text="Single-Predict",command=on_predict_single).grid(row=9,column=1,padx=10,pady=5)
    ttk.Button(frame_data_fields,text="Multi-Predict & Plot",command=on_predict_multi).grid(row=9,column=2,padx=10,pady=5)   

    ttk.Label(frame_data_fields,text="Results").grid(row=10,column=1,padx=10,pady=5)



    #---------------------------------------------------------------------------------------------

    result_values = ttk.Label(frame_data_fields,text="")
    result_values.grid(row=11,column=1,padx=10,pady=5)

# endregion SINGLE_DAY
#------------------------------------------------------------------------------------------------
# region MULTI-DAY

# regionend MULTI-DAY

    # Run the app loop
    root.mainloop()

if __name__ == "__main__":
    run_app()
