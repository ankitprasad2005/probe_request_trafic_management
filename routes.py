from flask import Flask, jsonify, request
import serial
import time
from collections import deque
import threading
import random

app = Flask(__name__)

st, nd, stp = 5, 30, 3

# Initialize serial port (update with your port and baud rate)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)

# Deque to store the MAC addresses with their timestamps
mac_addresses = deque()

# Function to parse the serial output and extract MAC addresses
def parse_serial_data(line):
    parts = line.strip().split('|')
    if len(parts) == 2:
        mac = parts[0].split(': ')[1].strip()
        rssi = parts[1].split(': ')[1].strip()
        return mac, rssi
    return None, None

# Function to get the number of unique MAC addresses in the last 60 seconds
def unique_mac_count():
    current_time = time.time()
    # Remove MAC addresses older than 60 seconds
    while mac_addresses and current_time - mac_addresses[0][1] > 60:
        mac_addresses.popleft()

    # Get unique MAC addresses
    unique_macs = set(mac for mac, timestamp in mac_addresses)
    return len(unique_macs)

# Function to continuously read from the serial port
def read_serial():
    while True:
        line = ser.readline().decode('utf-8')
        if line:
            mac, rssi = parse_serial_data(line)
            if mac:
                current_time = time.time()
                mac_addresses.append((mac, current_time))
        time.sleep(1)

# Start a background thread to read from the serial port
threading.Thread(target=read_serial, daemon=True).start()

def random_int():
    return random.randint(st, nd)

@app.route('/unique_macs', methods=['GET'])
def get_unique_macs():
    count = unique_mac_count()
    return jsonify({"unique_mac": count})

@app.route('/random_int', methods=['GET'])
def get_random_integer():
    start = request.args.get('start', default=st, type=int)
    end = request.args.get('end', default=nd, type=int)
    step = request.args.get('step', default=stp, type=int)
    
    if 'last_value' not in get_random_integer.__dict__:
        get_random_integer.last_value = random.randint(start, end)
    
    direction = random.choice([-1, 1])
    new_value = get_random_integer.last_value + direction * step
    
    if new_value < start:
        new_value = start
    elif new_value > end:
        new_value = end
    
    get_random_integer.last_value = new_value
    return jsonify({"random_int": new_value})


# @app.route('/north', methods=['GET'])
# def north():
#     count = unique_mac_count()
#     return jsonify({"trafic": count})

@app.route('/north', methods=['GET'])
def north():
    start = request.args.get('start', default=st, type=int)
    end = request.args.get('end', default=nd, type=int)
    step = request.args.get('step', default=stp, type=int)
    
    if 'last_value' not in get_random_integer.__dict__:
        get_random_integer.last_value = random.randint(start, end)
    
    direction = random.choice([-1, 1])
    new_value = get_random_integer.last_value + direction * step
    
    if new_value < start:
        new_value = start
    elif new_value > end:
        new_value = end
    
    get_random_integer.last_value = new_value
    return jsonify({"trafic": new_value})

@app.route('/south', methods=['GET'])
def south():
    start = request.args.get('start', default=st, type=int)
    end = request.args.get('end', default=nd, type=int)
    step = request.args.get('step', default=stp, type=int)
    
    if 'last_value' not in get_random_integer.__dict__:
        get_random_integer.last_value = random.randint(start, end)
    
    direction = random.choice([-1, 1])
    new_value = get_random_integer.last_value + direction * step
    
    if new_value < start:
        new_value = start
    elif new_value > end:
        new_value = end
    
    get_random_integer.last_value = new_value
    return jsonify({"trafic": new_value})

@app.route('/east', methods=['GET'])
def east():
    start = request.args.get('start', default=st, type=int)
    end = request.args.get('end', default=nd, type=int)
    step = request.args.get('step', default=stp, type=int)
    
    if 'last_value' not in get_random_integer.__dict__:
        get_random_integer.last_value = random.randint(start, end)
    
    direction = random.choice([-1, 1])
    new_value = get_random_integer.last_value + direction * step
    
    if new_value < start:
        new_value = start
    elif new_value > end:
        new_value = end
    
    get_random_integer.last_value = new_value
    return jsonify({"trafic": new_value})

@app.route('/west', methods=['GET'])
def west():
    start = request.args.get('start', default=st, type=int)
    end = request.args.get('end', default=nd, type=int)
    step = request.args.get('step', default=stp, type=int)
    
    if 'last_value' not in get_random_integer.__dict__:
        get_random_integer.last_value = random.randint(start, end)
    
    direction = random.choice([-1, 1])
    new_value = get_random_integer.last_value + direction * step
    
    if new_value < start:
        new_value = start
    elif new_value > end:
        new_value = end
    
    get_random_integer.last_value = new_value
    return jsonify({"trafic": new_value})

# @app.route('/north', methods=['GET'])
# def north():
#     random_value = random.randint(st, nd)
#     return jsonify({"trafic": random_value})

# @app.route('/south', methods=['GET'])
# def south():
#     random_value = random.randint(st, nd)
#     return jsonify({"trafic": random_value})

# @app.route('/east', methods=['GET'])
# def east():
#     random_value = random.randint(st, nd)
#     return jsonify({"trafic": random_value})

# @app.route('/west', methods=['GET'])
# def west():
#     random_value = random.randint(st, nd)
#     return jsonify({"trafic": random_value})


if __name__ == '__main__':
    app.run(debug=True)
