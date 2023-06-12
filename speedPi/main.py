import time
import pygame

# If set to True, use keyboard input for gates
debugMode = True

if not debugMode:
    import RPi.GPIO as GPIO

# Pin numbers for the gates
gate1Pin = 2
gate2Pin = 3

# The distance between the two gates in centimeters
distanceCM = 100

# Maximum allowable time for a measurement or display in seconds
max_measurement_time = 4
max_display_time = 1

# Measurement delay for debouncing in seconds
measurement_delay = 0.1

# Speed related variables
speed = 0
current_speed = 0
previous_speed = 0

# Timing variables
start_time = 0
display_start_time = 0

# Gate status variables
gate1 = 0
gate2 = 0
gate_to_check = 0
active_measurement = False


def setup():
    if not debugMode:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gate1Pin, GPIO.IN)
        GPIO.setup(gate2Pin, GPIO.IN)


def update_speed():
    global current_speed, previous_speed, display_start_time

    measure()

    if current_speed != previous_speed:
        display_start_time = time.time()  # Reset and start the display timer
        set_speed()
        previous_speed = current_speed
        time.sleep(measurement_delay)  # Delay for debouncing

    if not active_measurement:
        check_display_time()


def check_display_time():
    global current_speed, previous_speed, display_start_time

    if current_speed != 0 and time.time() - display_start_time > max_display_time:
        previous_speed = current_speed
        current_speed = 0  # Set current speed to 0
        display_start_time = 0  # Reset display timer


def set_speed():
    global speed, current_speed
    speed = current_speed


def calculate_speed(current_time):
    # convert cm to m for the calculation
    distanceM = distanceCM / 100
    return distanceM / current_time * 3.6  # Calculate speed and convert from m/s to km/h


def measure():
    global gate1, gate2, start_time, active_measurement, gate_to_check, current_speed

    if not debugMode:
        gate1 = GPIO.input(gate1Pin)
        gate2 = GPIO.input(gate2Pin)

    # Debouncing the input
    time.sleep(measurement_delay)
    if not debugMode and (gate1 != GPIO.input(gate1Pin) or gate2 != GPIO.input(gate2Pin)):
        return

    if not active_measurement:
        if gate1 == 1 or gate2 == 1:
            start_time = time.time()
            gate_to_check = 2 if gate1 == 1 else 1
            active_measurement = True
    else:
        stop_signal = gate1 if gate_to_check == 1 else gate2
        if stop_signal == 1:
            current_speed = calculate_speed(time.time() - start_time)
            active_measurement = False
            gate_to_check = 0
        elif time.time() - start_time > max_measurement_time:
            start_time = 0
            active_measurement = False


def draw(screen):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 100)
    text_surface = font.render(f"{speed:.2f} km/h", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    screen.blit(text_surface, text_rect)
    pygame.display.flip()


def main():
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
