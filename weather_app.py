import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

owm = pyowm.OWM('OWM_Api_Key')
mgr = owm.weather_manager()

def plot_bar_chart(days, temp_min, temp_max, unit):
    plt.figure(figsize = (10, 5))
    x = np.arange(len(days))  # label locations
    width = 0.3 # width of the bars

    plt.bar(x - width / 2 , temp_min, width=width, label = 'Min Temp', color = 'skyblue')
    plt.bar(x + width / 2 , temp_max, width=width, label = 'Max Temp', color = 'orange', alpha = 0.7)
    plt.xlabel('Date')
    plt.ylabel(f'Temperature ({unit})')
    plt.title('Five day forecast (Bar Chart)')
    plt.legend()
    plt.xticks(x, days, rotation = 45)
    plt.tight_layout()
    st.pyplot(plt)

def plot_line_chart(days, temp_min, temp_max, unit):
    plt.figure(figsize = (10, 5))
    plt.plot(days, temp_min, label = 'Min Temp', color = 'skyblue',marker = 'o')
    plt.plot(days, temp_max, label = 'Max Temp', color = 'orange', alpha = 0.7, marker = 'o')
    plt.xlabel('Date')
    plt.ylabel(f'Temperature ({unit})')
    plt.title('Five day forecast (Bar Chart)')
    plt.legend()
    plt.xticks(rotation = 45)
    plt.tight_layout()
    st.pyplot(plt)

st.title("5 Day Weather Forecast")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")


place = st.text_input("NAME OF THE CITY :", "")
# if place == None:
#     st.write("Input a CITY!")

unit = st.selectbox("Select Temperature Unit",("Celsius","Fahrenheit"))
g_type = st.selectbox("Select Graph Type",("Line Graph","Bar Graph"))
if st.button("Get Weather"):
    if place:
        try:
            forecast = mgr.forecast_at_place(place, '3h').forecast
            daily_min = {}
            daily_max = {}
            # Aggregate min and max temps for each day
            for weather in forecast.weathers:
                date = datetime.fromtimestamp(weather.reference_time()).strftime('%Y-%m-%d')
                temps = weather.temperature('celsius') if unit == "Celsius" else weather.temperature('fahrenheit')
                temp_min = temps['temp_min']
                temp_max = temps['temp_max']
            

                if date in daily_min:
                    daily_min[date] = min(daily_min[date], temp_min)
                    daily_max[date] = max(daily_max[date], temp_max)
                else:
                    daily_min[date] = temp_min
                    daily_max[date] = temp_max

            

            # Only take next 5 days
            days = list(daily_min.keys())[:5]
            temp_min_list = [daily_min[day] for day in days]
            temp_max_list = [daily_max[day] for day in days]
            
            st.write(f"### Temperature forecast for {place}")
                # Plot the graph
            if g_type == "Bar Graph":
                plot_bar_chart(days, temp_min_list, temp_max_list, unit)
            else:
                plot_line_chart(days, temp_min_list, temp_max_list, unit)

            st.title("Minimum and Maximum Temperature:")
            for date in days:
                st.write(f"{daily_min[date]}°C --- {daily_max[date]}°C")    

        except Exception as e:
            st.error(f"Error fetching data: {e}")
    

        st.title(" Impending Temperature Changes:")
        try:
            forcaster = mgr.forecast_at_place(place, '3h')
            if forcaster.will_have_clear():
                st.write("Weather Clear!")
            if forcaster.will_have_clouds():
                st.write("It's Cloudy!")
            if forcaster.will_have_fog():
                st.write("It's Foggy!")
            if forcaster.will_have_rain():
                st.write("It's Rainy!")
            if forcaster.will_have_snow():
                st.write("It's Snowy!")
        
        except Exception as e:
            st.error(f"Error fetching data: {e}")

        st.title("Sun Rise and Sun Set Timings:")
        try:
            observation = mgr.weather_at_place(place)
            weather_data = observation.weather

            sunrise = weather_data.sunrise_time('iso')
            sunset = weather_data.sunset_time('iso')

            st.write(f"Sunrise in {place}: {sunrise}")
            st.write(f"Sunset in {place}: {sunset}")

        except Exception as e:
            st.error(f"Error fetching data: {e}")

        st.title("Cloud Coverage, Wind Speed and Wind Direction:")
        try:
            cloud_coverage = weather_data.clouds
            st.write(f"Cloud Coverage in {place} is {cloud_coverage}")

            wind = weather_data.wind()
            speed = wind.get('speed')
            direction = wind.get('deg')
            st.write(f"Wind Speed in {place} is {speed} in {direction}°")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

    else:
        st.warning("👈 Please enter a CITY to continue.")