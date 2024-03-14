import os
import requests
import streamlit as st
import pandas as pd
import pymysql
import altair as alt
from utils.recommender import cloth_recommend

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=3306,
        user=os.getenv("DB_USER"),  
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
    )


def search_location(location):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            if location.isdigit():
                cursor.execute(
                    "SELECT * FROM postcodes_geo WHERE postcode = %s",
                    (location),
                )
            else:
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


def display_location_weather(location, demo = False):
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
    weather_display_ui(location_found[2], location_found[3], weather, demo)


def weather_display_ui(location, state, weather_data, demo = False):
    with st.container(border=True):
        st.subheader(f"**{location}**({state})", divider="rainbow")
        uvi = weather_data[0][1]
        recommendation,_ = cloth_recommend(round(uvi))
        if demo:
            col1, col2 = st.columns([1,2])
            col1.metric("UV Index", f"{uvi}")
            with col2:
                html = f"""
                 <p style="font-family:Helvetica; color: #393939; font-size: 0.8rem;text-align: left">
                    Clothing Advice
                </p>
                <p style="font-family:Helvetica; color: #393939; font-size: 0.8rem;text-align: left">
                    {recommendation}
                </p>
                """
                st.markdown(html, unsafe_allow_html= True)
        else:
            col1, col2, col3 = st.columns([1,1,1.5])
            col1.metric("UV Index", f"{uvi}")
            col2.metric("Temperature", f"{weather_data[0][2]} °C")
            col3.metric("Weather", f"{weather_data[0][3]}")
            st.divider()
            html = f"""
                 <p style="font-family:Helvetica; color: #393939; font-size: 1.3rem;text-align: left">
                    Clothing Advice
                </p>
                <p style="font-family:Helvetica; color: #393939; font-size: 1rem;text-align: left">
                    {recommendation}
                </p>
                """
            st.markdown(html, unsafe_allow_html= True)
            st.divider()
            hourly_forecast = weather_data[1]
            hourly_forecast["UV Index"] = hourly_forecast["uvi"][:23]
            hourly_forecast["Temperature"] = hourly_forecast["temp"][:23]
            hourly_forecast["Time"] = pd.to_datetime(
                hourly_forecast["dt"], unit="s", utc=True
            )
            hourly_forecast["Time"] = hourly_forecast["Time"][:23]
            hourly_forecast["ymin"] = 8
            hourly_forecast["y10"] = 10
            hourly_forecast["y12"] = 12
            chart = alt.Chart(hourly_forecast).mark_line(point = alt.OverlayMarkDef(filled=False,fill = "white")).encode(
                    x=alt.X('Time:T',axis=alt.Axis(format = "%a %I:%M %p",tickCount = 4)),
                    y=alt.Y('UV Index:Q', scale = alt.Scale(domainMin=0)),
                    tooltip= [alt.Tooltip('Time:T', format="%a %I:%M %p"),alt.Tooltip('UV Index:Q', format='.1f')],
                    color=alt.value("gray")  
            ).properties(title = "24 Hour UV Forecast")

            chart.configure_title(
                fontSize=18,
                font = "Helvetica",
                color = "Gray"
            )
            high_uv = alt.Chart(hourly_forecast).mark_area(color="red", opacity = 0.6).encode(
                    x=alt.X('Time:T',axis=alt.Axis(format = "%a %I:%M %p",tickCount = 4), title = "Day, Time"),
                    y=alt.Y('ymin:Q', title = "UV Index"),
                    y2="y10:Q",
                    tooltip=alt.value(None) 
            )

            ultra_uv = alt.Chart(hourly_forecast).mark_area(color="indigo",opacity=0.6).encode(
                    x=alt.X('Time:T',axis=alt.Axis(format = "%a %I:%M %p",tickCount = 4), title = "Day, Time"),
                    y=alt.Y('y10:Q', title = "UV Index"),
                    y2="y12:Q",
                    tooltip=alt.value(None)  
            )
            chart_combined = high_uv + ultra_uv + chart
            st.altair_chart(chart_combined,use_container_width=True)

            temp_chart = alt.Chart(hourly_forecast).mark_line(point = alt.OverlayMarkDef(filled=False,fill = "white")).encode(
                    x=alt.X('Time:T',axis=alt.Axis(format = "%a %I:%M %p",tickCount = 4)),
                    y=alt.Y('Temperature:Q', scale = alt.Scale(domainMin=0),title = "Temperature (°C)"),
                    tooltip= [alt.Tooltip('Time:T', format="%a %I:%M %p"), alt.Tooltip('Temperature:Q', format='.1f')],
                    color=alt.value("red") 
            ).properties(title = "24 Hour Temperature Forecast")

            st.altair_chart(temp_chart,use_container_width=True)
                #st.line_chart(hourly_forecast, x="Time", y="UV Index", color="#520160")
                #st.line_chart(hourly_forecast, x="Time", y="Temperature", color="#ffa500")

