from djitellopy import tello
from time import sleep

switch = 0
def intialize():
    global tc
    tc = tello.Tello()
    tc.connect()
    print(tc.get_battery())

flying = False
def takeOff():
    global flying
    if flying == False:
        tc.takeoff()
        flying = True

def land():
    global flying
    if flying:
        tc.land()
        flying = False

def moveForward():
    tc.send_rc_control(0, 15, 0, 0)

def moveBackward():
    tc.send_rc_control(0,-15,0,0)
def moveLeft():
    tc.send_rc_control(-50,0,0,0)
def moveRight():
    tc.send_rc_control(50,0,0,0)

def wait():
    sleep(8)
    land()

# def getKeyboardInput():
#
#     if kp.getKey("LEFT"):
#         moveLeft()
#     elif kp.getKey("RIGHT"):
#         moveRight()
#
#
#     if kp.getKey("UP"):
#         moveForward()
#     if kp.getKey("s"):
#         global switch
#         switch += 1
#         startStop(switch)
#
#
# # While file is running.




