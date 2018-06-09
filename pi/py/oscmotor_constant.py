import OSC
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from flask import jsonify

import time
import atexit
import thread

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

class Shape:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.description = "This shape has not been described yet"
        self.author = "Nobody has claimed to make this shape yet"
        self.stepper = mh.getStepper(200, 1)
        self.stepper.setSpeed(10000)
        self.dir = Adafruit_MotorHAT.FORWARD
        self.style = Adafruit_MotorHAT.SINGLE
        self.state = 0
        print('init');

    def area(self):
        return self.x * self.y

    def perimeter(self):
        return 2 * self.x + 2 * self.y
        
    def run(self):
        while True:
            if self.state == 1:
                self.stepper.step(1, self.dir,  self.style)
        
    def describe(self, data):
        print(self.description)
        print(data)
        
        self.state = 1
        
        self.stepper.setSpeed(data[0])
        
        self.dir = Adafruit_MotorHAT.FORWARD
        if data[1] == 'backward':
            self.dir = Adafruit_MotorHAT.BACKWARD
        
            
        self.style = Adafruit_MotorHAT.SINGLE
        if data[2] == 'double':
            self.style = Adafruit_MotorHAT.DOUBLE
        if data[2] == 'interleave':
            self.style = Adafruit_MotorHAT.INTERLEAVE
        if data[2] == 'microstep':
            self.style = Adafruit_MotorHAT.MICROSTEP
        

    def stop(self):
        self.state = 0

    def scaleSize(self, scale):
        self.x = self.x * scale
        self.y = self.y * scale
        

rectangle = Shape(100, 45)

thread.start_new_thread ( rectangle.run, () )

def handler(addr, tags, data, client_address):
	rectangle.describe(data)

def stophandle(addr, tags, data, client_address):
	rectangle.stop()

	
if __name__ == "__main__":
    s = OSC.OSCServer(('0.0.0.0', 2222)) 
    s.addMsgHandler('/startup', handler)
    s.addMsgHandler('/stop', stophandle)     
    s.serve_forever()
