import pygame
import time
import RPi.GPIO as GPIO

# measurement variables
gate1, gate2 = 0, 0  # 0 = free -- 1 = closed
gate1Pin, gate2Pin = 2, 3
currentSpeed, previousSpeed = 10.0, 0.0
distanceCM = 100
gateToCheck, stopSignal = 0, 0
currentTime = 0

maxMeasurementTime = 4
maxDisplayTime = 1
activeMeasurement = False
measurementDelay = 100

# styling variables
speed = 0.0  # measured Speed
unit = "km/h"
fontScalerSpeed = 3
textMiddleScaler = 40
textSpacingScaler = 30

# debug mode
debugMode = True

def setup():
    if not debugMode:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gate1Pin, GPIO.IN)
        GPIO.setup(gate2Pin, GPIO.IN)

def debounce_read(pin, num_samples=5, delay_time=10):
    """Read input from pin taking into account debounce"""
    measurements = [GPIO.input(pin) for _ in range(num_samples)]
    return 1 if measurements.count(1) > num_samples / 2 else 0

def update_speed():
    global currentSpeed, previousSpeed, speed, activeMeasurement
    measure()

    if currentSpeed != previousSpeed:
        previousSpeed = currentSpeed
        speed = currentSpeed
        time.sleep(measurementDelay / 1000.0)  # sleep expects time in seconds

    if not activeMeasurement:
        check_display_time()

def check_display_time():
    global currentSpeed, previousSpeed
    if currentSpeed != 0 and display_timer_elapsed > maxDisplayTime:
        previousSpeed = currentSpeed
        currentSpeed = 0

def calculate_speed():
    return abs((distanceCM / 100) / (currentTime / 10) * 3.6)  # cm to m, microsec to sec, m/sec to km/h

def measure():
    global gate1, gate2, stopSignal, currentTime, previousSpeed, currentSpeed, activeMeasurement, gateToCheck
    gate1 = debounce_read(gate1Pin) if not debugMode else gate1
    gate2 = debounce_read(gate2Pin) if not debugMode else gate2

    stopSignal = gate1 if gateToCheck == 1 else gate2 if gateToCheck == 2 else 0

    if not activeMeasurement and (gate1 == 1 or gate2 == 1):
        speed_timer_start = time.time()
        gateToCheck = 2 if gate1 == 1 else 1
        activeMeasurement = True

    elif activeMeasurement:
        if stopSignal == 1:
            currentTime = (time.time() - speed_timer_start) * 1e6  # convert sec to microsec
            previousSpeed = currentSpeed
            currentSpeed = calculate_speed()
            activeMeasurement = False
            gateToCheck = 0

        elif (time.time() - speed_timer_start) > maxMeasurementTime:
            speed_timer_start = time.time()
            activeMeasurement = False

def draw(screen):
    global speed
    screen.fill((0, 0, 0))

    if pygame.font:
        font = pygame.font.Font(None, int(screen.get_height() / fontScalerSpeed))
        text = "{:.2f} {}".format(speed, unit)
        text_surface = font.render(text, True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

def main():
    global gate1, gate2
    setup()

    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if debugMode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gate1 = 1 - gate1
                if event.key == pygame.K_2:
                    gate2 = 1 - gate2

        update_speed()
        draw(screen)

if __name__ == "__main__":
    main()
