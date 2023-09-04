import pygame
import time

# Uncomment this when you are ready to use GPIO
# import RPi.GPIO as GPIO

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

display_timer_start = None
measurement_started_time = None

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
    global currentSpeed, display_timer_start
    if display_timer_start is not None and (time.time() - display_timer_start) > maxDisplayTime:
        currentSpeed = 0.0

def calculate_speed():
    return abs((distanceCM / 100) / (currentTime / 10) * 3.6)  # cm to m, microsec to sec, m/sec to km/h



def measure():
    global gate1, gate2, stopSignal, currentTime, previousSpeed, currentSpeed, activeMeasurement, gateToCheck, speed_timer_start, display_timer_start, measurement_started_time

    gate1 = debounce_read(gate1Pin) if not debugMode else gate1
    gate2 = debounce_read(gate2Pin) if not debugMode else gate2
    
    if gateToCheck == 1:
        stopSignal = gate1
    elif gateToCheck == 2:
        stopSignal = gate2
    else:
        stopSignal = 0

    if not activeMeasurement and (gate1 == 1 or gate2 == 1):
        speed_timer_start = time.time()
        measurement_started_time = speed_timer_start
        print("start measurement")
        gateToCheck = 2 if gate1 == 1 else 1
        activeMeasurement = True

    elif activeMeasurement:
        # Add a delay before checking the stop gate (e.g., 0.1 second).
        # This will ensure the start gate's prolonged signal doesn't immediately trigger the stop.
        if time.time() - measurement_started_time < 0.1:
            return
        
        if stopSignal == 1:
            print("stop measurement")
            currentTime = (time.time() - speed_timer_start) * 1e6  # convert sec to microsec
            previousSpeed = currentSpeed
            currentSpeed = calculate_speed()
            display_timer_start = time.time()
            activeMeasurement = False
            gateToCheck = 0

        elif (time.time() - speed_timer_start) > maxMeasurementTime:
            print("measurement timeout")
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
    screen = pygame.display.set_mode((600, 300), pygame.RESIZABLE)

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
