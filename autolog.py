import json
from networktables import NetworkTables

json_path = input("Enter the JSON file path: ")
json_file = open(json_path,"r")
json_string = json_file.read().replace('\n', '')
trial_object = json.loads(json_string)

ip = input("Robot IP Address: ")

NetworkTables.initialize(server=ip)


def valueChanged(table, key, value, isNew):
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))


def connectionListener(connected, info):
    print(info, "; Connected=%s" % connected)


NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

sd = NetworkTables.getTable("SmartDashboard")
sd.addEntryListener(valueChanged)

while True:
    time.sleep(1)

maxAcceleration

"autolog" "maxAcceleration"