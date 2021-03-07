import json
from networkTables import NetworkTables
import time

# Grabs the json file
json_path = input("Enter the JSON file path: ")

json_file = open(json_path,"r")

json_string = json_file.read().replace('\n', '')
# Reads it into an object
trial_object = json.loads(json_string)

# Grabs the IP address
ip = input("Robot IP Address: ")

# Initializes network tables and begins to try to connect. 
NetworkTables.initialize(server=ip)

def valueChanged(table, key, value, isNew):
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))

# If the connection has been established
isConnected = False

# Prints status and updates isConnected when called. 
def connectionListener(connected:bool, info):
    print(info, "; Connected=%s" % connected)
    global isConnected
    if connected: isConnected = True

# Adds a connection listener. 
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# Grabs the autolog table
sd = NetworkTables.getTable("autolog")

sd.addEntryListener(valueChanged)

print("Trying to connect...")
while not isConnected:
    print("Waiting for connection...")
    time.sleep(1)
print("Connection established!")

queue = NetworkTables.getTable("autolog")

for line in trial_object :
    # We aren't done yet - we haven't even started! 
    queue.putBoolean("finished", False)
    queue.putBoolean("started", False)
    # Sets max acceleration
    queue.putNumber("maxAcceleration", line.get("maxAcceleration"))
    # Sets max velocity
    queue.putNumber("maxVelocity", line.get("maxVelocity"))
    print("Data sent!")
    # Waits for task to start (when started is set to True server-side)
    while not queue.getBoolean("started", False):
        time.sleep(1)
    # Waits for task to finish (when finished is set to True server-side)
    # Yes, finished is consistent with autonomousInit being set to false
    # after being set to true, but it might not always be. Not having this
    # hack will make this code more robust, so we won't need to change as 
    # much in the long run - if we're doing a teleop test, for example,
    # or if we don't want to disable autonomous. 
    while not queue.getBoolean("finished", False):
        time.sleep(1)
    print("Task finished!")
print("all tasks finished!")
