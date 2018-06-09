import OSC
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from flask import jsonify

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(1000)             # 30 RPM

def handler(addr, tags, data, client_address):
    print(data)
    txt = "OSCMessage '%s' from %s: " % (addr, client_address)
    txt += str(data)
    dir = Adafruit_MotorHAT.FORWARD
    if data[1] == 'backward':
		dir = Adafruit_MotorHAT.BACKWARD
    
    style = Adafruit_MotorHAT.SINGLE
    if data[2] == 'double':
		style = Adafruit_MotorHAT.DOUBLE
    if data[2] == 'interleave':
		style = Adafruit_MotorHAT.INTERLEAVE
    if data[2] == 'microstep':
		style = Adafruit_MotorHAT.MICROSTEP

    
    myStepper.step(data[0], dir,  style)
    


if __name__ == "__main__":
    s = OSC.OSCServer(('0.0.0.0', 2222)) 
    s.addMsgHandler('/startup', handler)     
    s.serve_forever()
