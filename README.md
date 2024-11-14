Probe request trafic management
----


## Dependencies:
- flask 
- pyserial
- streamlit


## How to run
Build and upload the ```probe/probe.ino``` to a ESP32.

To run backend (apis):
```
python routes.py
```

To run frountend:
```
streamlit run app.py
```

## About
The ESP32 spits out serially the MAC address its RSSI (reversed signal strength indicator).

The ```routes.py``` creates api endpoints: ```/north /south /east /west```.
The code reades serial out from the ESP32 gets the count of unique MAC addresses in 60 sec.