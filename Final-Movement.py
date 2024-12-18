from netmiko import ConnectHandler
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime
from Config import deviceType, host, username_, password_, checkTime, sleepTime, maxHours, minHours, interfaces
import logging


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

now = datetime.now()

# REQUIRED TO CONNECT TO SWITCH
net_connect = ConnectHandler(
    device_type = deviceType,
    host = host,
    username = username_,
    password = password_,
)



def Close(interfaces):
    # repeates for every interface(port)
    for interface in interfaces:
        # Shutdown the interface
        commands = [f"interface {interface}", "shutdown"]
        output = net_connect.send_config_set(commands)
        logging.info(f'{interface} status: offline')
        
        print(output)
        


def Open(interface):
    # Opens the port
    commands = [f"interface {interface}", "no shutdown"]
    output = net_connect.send_config_set(commands)
    print(output)
        
# Runs command, Go through for loop grabbing power from every line and storing. List in list, with string.
# def GrabPower():
#     commands = [f"show power inline | inc Gi"]
#     output = net_connect.send_config_set(commands)
#     output_list = output.splitlines()



pir = MotionSensor(4)
timer = 0
now = datetime.now()

def TurnOn():

    print("Waiting for motion")
    pir.wait_for_motion()    
    for interface in interfaces:
            # Gets the current state of the port
            output = net_connect.send_command(f"show interface {interface}")
            
            # Checks if the port is off If yes Then it opens it
            if "disabled" in output:
                print(f"{interface} is administratively down")
                Open(interface)
                print(f"{interface} has been enabled, please wait for AP to boot")
            else:
                print(f"{interface} is online")
                logging.info(f'{interface} status: online')
                


def Timer():
    check = True
    print("Pi will now sleep for 10 minutes")
    sleep(sleepTime)  # sleeping for 10 minutes
    print("Pi has exited 10 minute Timeout and is awaiting motion")
    timer = 0
    
    
    while check == True:
        if pir.value == True:
            pass
            check = False
        elif pir.value == False and timer >= checkTime: # if doesn't turn on for 5 minutes
            Close(interfaces)
            check = False
        else:
            sleep(1)
            timer += 1


# when out of working hours the code is running otherwise the ports are left open
while True:
    TurnOn()
    while now.hour >= maxHours or now.hour < minHours:
        TurnOn()
        Timer()
