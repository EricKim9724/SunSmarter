from utils.authentication import get_connection
import os
import requests
import streamlit as st
import pandas as pd

def search_location(location):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM postcodes_geo WHERE LOWER(suburb) = %s",
                (location.lower()),
            )
            result = cursor.fetchall()
            if result:
                return result
            else:
                return None
    finally:
        connection.close()


def get_weather_data(lat, lon):
    api_key = os.getenv("WEATHER_API_KEY")
    request_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    try:
        response = requests.get(request_url)
        response_data = response.json()
        current_info = [response_data["current"][key] for key in ["dt", "uvi", "temp"]]
        current_info.append(response_data["current"]["weather"][0]["main"])
        tz_offset = response_data["timezone_offset"]
        hourly_info = pd.DataFrame(response_data["hourly"])
        return (current_info, hourly_info, tz_offset)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


def display_location_weather(location):
    search = search_location(location)
    if search == None:
        st.write(
            f"{location} is not found in our database, please check spelling and try again."
        )
        return None
    elif len(search) > 1:
        select_match = st.selectbox(
            "Multiple matching locations found, please select:",
            [(i, row[2], row[1], row[3]) for i, row in enumerate(search)],
        )
        location_found = search[select_match[0]]
    else:
        location_found = search[0]
    lat, lon = location_found[-2], location_found[-1]
    weather = get_weather_data(lat, lon)
    weather_display_ui(location_found[2], location_found[3], weather)


def weather_display_ui(location, state, weather_data):
    with st.container(border=True):
        st.subheader(f"**Currently in {location}({state})**", divider="rainbow")
        col1, col2, col3 = st.columns(3)
        col1.metric("UV Index", f"{weather_data[0][1]}")
        col2.metric("Temperature", f"{weather_data[0][2]} °C")
        col3.metric("Weather", f"{weather_data[0][3]}")
        with st.expander("Forecast", True):
            hourly_forecast = weather_data[1]
            hourly_forecast["UV Index"] = hourly_forecast["uvi"]
            hourly_forecast["Temperature"] = hourly_forecast["temp"]
            hourly_forecast["Time"] = pd.to_datetime(
                hourly_forecast["dt"] + weather_data[2], unit="s", utc=True
            )
            st.line_chart(hourly_forecast, x="Time", y="UV Index", color="#520160")
            st.line_chart(hourly_forecast, x="Time", y="Temperature", color="#ffa500")

