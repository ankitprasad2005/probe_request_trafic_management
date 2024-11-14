import streamlit as st
import requests
import time

# Function to get the number of cars from the API
def get_number_of_cars(road):
    response = requests.get(f'http://127.0.0.1:5000/{road}')
    if response.status_code == 200:
        return response.json().get('trafic', 0)
    else:
        return 0

# Function to determine traffic light color based on the total number of cars
def get_traffic_light_color(traffic_data):
    sorted_roads = sorted(traffic_data.items(), key=lambda x: x[1]['number_of_cars'])
    for i, (road, data) in enumerate(sorted_roads):
        if i < 2:
            traffic_data[road]['light_color'] = 'red'
        elif i < 3:
            traffic_data[road]['light_color'] = 'yellow'
        else:
            traffic_data[road]['light_color'] = 'green'
    return traffic_data

# Streamlit app
st.title('Traffic Light Control System')

roads = ['north', 'south', 'east', 'west']

# Initialize a placeholder for the traffic data
traffic_data_placeholder = st.empty()

def refresh_traffic_data():
    traffic_data = {}

    for road in roads:
        number_of_cars = get_number_of_cars(road)
        traffic_data[road] = {
            'number_of_cars': number_of_cars,
        }

    traffic_data = get_traffic_light_color(traffic_data)

    return traffic_data

while True:
    traffic_data = refresh_traffic_data()
    
    # Display the traffic lights in a plus form
    with traffic_data_placeholder.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write("")
        
        with col2:
            st.write(f"Road: North")
            st.write(f"Number of Cars: {traffic_data['north']['number_of_cars']}")
            st.write(f"Traffic Light: {traffic_data['north']['light_color'].capitalize()}")
            st.markdown(f"<div style='width: 50px; height: 50px; background-color: {traffic_data['north']['light_color']};'></div>", unsafe_allow_html=True)
        
        with col3:
            st.write("")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write(f"Road: West")
            st.write(f"Number of Cars: {traffic_data['west']['number_of_cars']}")
            st.write(f"Traffic Light: {traffic_data['west']['light_color'].capitalize()}")
            st.markdown(f"<div style='width: 50px; height: 50px; background-color: {traffic_data['west']['light_color']};'></div>", unsafe_allow_html=True)
        
        with col2:
            st.write("")
        
        with col3:
            st.write(f"Road: East")
            st.write(f"Number of Cars: {traffic_data['east']['number_of_cars']}")
            st.write(f"Traffic Light: {traffic_data['east']['light_color'].capitalize()}")
            st.markdown(f"<div style='width: 50px; height: 50px; background-color: {traffic_data['east']['light_color']};'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write("")
        
        with col2:
            st.write(f"Road: South")
            st.write(f"Number of Cars: {traffic_data['south']['number_of_cars']}")
            st.write(f"Traffic Light: {traffic_data['south']['light_color'].capitalize()}")
            st.markdown(f"<div style='width: 50px; height: 50px; background-color: {traffic_data['south']['light_color']};'></div>", unsafe_allow_html=True)
        
        with col3:
            st.write("")
        
    # Wait for a short period before refreshing
    time.sleep(4)
