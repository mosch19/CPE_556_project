import RPi.GPIO as GPIO
import threading
from time import sleep

class SensorInput:
    def __init__(self):
        setup()
        self.status = [False, False, False]
        self.update = True
        self.light = False
        self.air = False
        self.heat = False

    def get_status(self):
        return self.status

    def auto(self):
        self.status = auto_input(self.light, self.air, self.heat)[:]
        if self.update:
            threading.Timer(.3, self.auto).start()
        else:
            GPIO.cleanup()
    
    def light_on(self):
        self.light = True
        room_on()

    def light_off(self):
        self.light = False
        room_off()

    def air_on(self):
        self.air = True
        ac_on((0, 0, 1))

    def heat_on(self):
        self.heat = True
        ac_on((1, 0, 0))

    def ac_off(self):
        self.air = False
        self.heat = False
        ac_off()

    def start(self):
        setup()

    def restart(self):
        setup()
        self.update = True

    def stop(self):
        self.air = False
        self.light = False
        self.heat = False
        self.update = False

temp_dict = {'COLD': 26, 'MED':19, 'HOT':13}
led_colors = {'R':23, 'G':24, 'B':25}

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(22, GPIO.OUT)

    for val in temp_dict:
        GPIO.setup(temp_dict[val], GPIO.IN)

    for val in led_colors:
        GPIO.setup(led_colors[val], GPIO.OUT)

def light_in():
    return GPIO.input(18)

def temp_in():
    return (GPIO.input(temp_dict.get('COLD')), GPIO.input(temp_dict.get('MED')), GPIO.input(temp_dict.get('HOT')))

def distance():
    return GPIO.input(20)

def room_on():
    GPIO.output(22, 1)

def room_off():
    GPIO.output(22, 0)

def ac_on(color):
    GPIO.output(led_colors.get('R'), 1 - color[0])
    GPIO.output(led_colors.get('G'), 1 - color[1])
    GPIO.output(led_colors.get('B'), 1 - color[2])

def ac_off():
    GPIO.output(led_colors.get('R'), 1)
    GPIO.output(led_colors.get('G'), 0)
    GPIO.output(led_colors.get('B'), 1)

def auto_input(light, air, heat):
    result = [False, False, False]
    if (light_in() == 1 and distance() == 0) or light:
        room_on()
        result[0] = True
    else:
        room_off()
    temps = temp_in()
    print temps
    if temps[0] == 1 or heat:
        ac_on((1, 0, 0))
        result[1] = True
    elif temps[2] == 1 or air:
        ac_on((0, 0, 1))
        result[2] = True
    elif temps[1] == 1:
        ac_off()
    return result

#setup()
#try:
#    while True:
#        print light_in(), distance()
#        if light_in() == 1 and distance() == 0:
#            room_on()
#        else:
#            room_off()
#        temps = temp_in()
#        if temps[0] == 1:
#            ac_on((1, 0, 0))
#        elif temps[1] == 1:
#            ac_off()
#        else:
#            ac_on((0, 0, 1))
#
#finally:
#    GPIO.cleanup()
