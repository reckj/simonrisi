import time
import pygame
import sys 


# Uncomment this when you are ready to use GPIO
#import RPi.GPIO as GPIO

# set debug mode to True to use keyboard input instead of GPIO
debugMode = True
debounceDelay = 0.01 #delay in seconds
measurementDelay = 1 #delay in seconds
measurementTimeout = 4 #timeout in seconds

# input pins
gate1Pin = 17
gate2Pin = 27

def setup():
    if not debugMode:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gate1Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(gate2Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#function that reads the pin and returns a 1 if the pin is high and a 0 if the pin is low
def readPin(pin):
    if debugMode:
        if pin == 1:
            if pygame.key.get_pressed()[pygame.K_1]:
                #print("1 key pressed")
                return 1
            else:
                return 0
        elif pin == 2:
            if pygame.key.get_pressed()[pygame.K_2]:
                #print("2 key pressed")
                return 1
            else:
                return 0
    else:
        return GPIO.input(pin)

#debounce function that checks if the gate is triggered 5 times in succession with a small delay and returns a 1 if it is triggered and 0 if it is not triggered
def debounce_read(gate):
    count = 0
    for i in range(5):

        if gate == 1:
            pinStatus = readPin(1)
        elif gate == 2:
            pinStatus = readPin(2)

        if pinStatus == 1:
            count += 1
        time.sleep(debounceDelay)
    if count >= 3:
        return 1
    else:
        return 0

#class that creates a timer object which has a start and stop and reset function and logic to check if the timer is running
class Timer:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.deltaT = 0
        self.running = False

    def start(self):
        if self.running == False:
            self.startTime = time.time()
            self.running = True
        else:
            print("Timer is already running")

    def stop(self):
        if self.running == True:
            self.endTime = time.time()
            self.deltaT = self.endTime - self.startTime
            self.running = False
        else:
            print("Timer is not running")

    def reset(self):
        self.startTime = 0
        self.endTime = 0
        self.deltaT = 0
        self.running = False

    def getTime(self):
        self.deltaT = time.time() - self.startTime
        return self.deltaT


#class that creates a speedgate object which has a update function that checks if the gate is triggered and updates the gate variable
class SpeedGate:
    def __init__(self):
        self.gate1 = 0 # 0 = closed, 1 = triggered/open
        self.gate2 = 0  # 0 = closed, 1 = triggered/open
        self.gateTriggered = 0 # 0 = no gate triggered, 1 = gate 1 triggered, 2 = gate 2 triggered
        self.currentSpeed = 0
        self.previousSpeed = 0
        self.distanceM = 1 # distance in meters
        self.state = 1 # 0 = idle, 1 = measuring
        self.lastMeasurement = 0
        
    def update(self):
        self.checkGate()
        #switch case for the speedgate state
        if self.state == 0:
            return
        elif self.state == 1:
            if time.time() - self.lastMeasurement > measurementDelay:
                self.measure(timerSpeed)
            return

    def changeState(self, state):
        self.state = state
    
    def getSpeed(self):
        return self.currentSpeed
    
    def checkGate(self):
        self.gate1 = debounce_read(1)
        self.gate2 = debounce_read(2)

    def calculateSpeed(self, timerSpeed):
        self.previousSpeed = self.currentSpeed
        self.currentSpeed = self.distanceM / timerSpeed.deltaT * 3.6
        print("current speed: ", self.currentSpeed)
    
    def measure(self, timerSpeed):
        #timer not started
        if timerSpeed.running == False:
            #case gate1 or gate1 is triggered
            if self.gate1 == 1:
                timerSpeed.reset()
                timerSpeed.start()
                self.gateTriggered = 1
                print("gate 1 triggered - start timer")
                return
            #case gate2 is triggered
            elif self.gate2 == 1:
                timerSpeed.reset()
                timerSpeed.start()
                self.gateTriggered = 2
                print("gate 2 triggered - start timer")
                return
        #timer started
        elif timerSpeed.running == True:
            #check if measurement timed out
            if timerSpeed.getTime() > measurementTimeout:
                timerSpeed.stop()
                print("measurement timed out")
                self.currentSpeed = 0
                print("current speed: ", self.currentSpeed)
                return
            if self.gateTriggered == 1:
                if self.gate2 == 1:
                    timerSpeed.stop()
                    self.calculateSpeed(timerSpeed)
                    self.lastMeasurement = time.time()
                    #self.changeState(0)
                    return
                else:
                    return
            elif self.gateTriggered == 2:
                if self.gate1 == 1:
                    timerSpeed.stop()
                    self.calculateSpeed(timerSpeed)
                    self.lastMeasurement = time.time()
                    #self.changeState(0)
                    return
                else:
                    return

                    
def draw(screen, speedGate):
    screen.fill((0, 0, 0))
    unit = "km/h"
    fontScalerSpeed = 4

    if pygame.font:
        font = pygame.font.Font(None, int(screen.get_height() / fontScalerSpeed))
        text = "{:.2f} {}".format(speedGate.getSpeed(), unit)
        text_surface = font.render(text, True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

#instances of the timer class
timerSpeed = Timer()
timerDisplay = Timer()

#instance of the speedgate class
speedGate = SpeedGate()




def main():
    setup()

    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((600, 300), pygame.RESIZABLE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        speedGate.update()
        draw(screen, speedGate)

if __name__ == "__main__":
    main()