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
            traffic_data[road]['light_color'] = 'green'
        elif i < 3:
            traffic_data[road]['light_color'] = 'yellow'
        else:
            traffic_data[road]['light_color'] = 'red'
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
    
    # Display the traffic lights
    with traffic_data_placeholder.container():
        for road, data in traffic_data.items():
            st.write(f"Road: {road.capitalize()}")
            st.write(f"Number of Cars: {data['number_of_cars']}")
            st.write(f"Traffic Light: {data['light_color'].capitalize()}")
            st.markdown(f"<div style='width: 50px; height: 50px; background-color: {data['light_color']};'></div>", unsafe_allow_html=True)
            st.write("---")

    # Wait for a short period before refreshing
    time.sleep(2)
    st.experimental_set_query_params()
