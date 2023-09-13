# '''
# regal.py

from interstate75 import Interstate75
import time
from machine import Pin, Timer
#import _thread

# Display definitions
i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
graphics = i75.display
MAGENTA = graphics.create_pen(255, 0, 255)
BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)
GREEN = graphics.create_pen(57, 255, 20)
RED = graphics.create_pen(255, 24, 24)
BLUE = graphics.create_pen(8, 51, 162)

# Timer definitions
total_time = 100
#est_time = time.localtime([2023,1,1,1,1,5,1,1])
est_time = time.localtime(65)
est_formatted_time = "{a:02d}:{b:02d}".format(a = est_time[4], b = est_time[5]%60)

# PLC definitions
## A0
## INICIO ciclo
## A1
## CUENTA pieza
## A2
## RESET general
delayed_pz = 0
on_time_pz = 0

def setup_display():
    graphics.clear()
    graphics.set_font("bitmap8")
    graphics.set_thickness(25)
    
def display_actual_time(formatted_time):
    graphics.set_pen(GREEN)
    graphics.text("T.Act: ", 1, 16, scale=1)
    graphics.text(formatted_time, 1, 24, scale=1)
    
def display_est_time():
    graphics.set_pen(WHITE)
    graphics.text("T.Est", 1, 0, scale=1)
    graphics.text(est_formatted_time, 1, 8, scale=1)

def display_curr_count():
    graphics.set_pen(MAGENTA)
    graphics.text("C:" + str(on_time_pz), 32, 4, scale=1)

def display_delayed_pz():
    # Imprimir cuenta de piezas retrasadas
    # Se incrementa cuando se detecta que sale una pieza
    # y el T.Act > T.Est
    graphics.set_pen(RED)
    delayed_pz_str = str(delayed_pz)
    graphics.text(delayed_pz_str, 32, 14, scale=2)

def time_tick(timer):
    global start_time, total_time
    current_time = time.time() # using the time() function will likely be more accurate than counting the ticks, plus we can mess with the tick frequency now.
    elapsed_time = current_time - start_time
    formatted_time = "{a:02d}:{b:02d}".format(a = elapsed_time//60, b = elapsed_time%60)
    graphics.set_pen(BLACK)
    graphics.clear()
    display_actual_time(formatted_time)
    display_est_time()
    display_curr_count()
    display_delayed_pz()
    i75.update(graphics)
    
def start_timer():
    Timer().init(freq=1, mode=Timer.PERIODIC, callback=time_tick)

# INICIO empieza timer
def GPIO_A0_callback(pin):
    pin.irq(handler=None)
    print("GPIO_A0_callback Falling edge detected for: ", pin)
    # Start timer
    global start_time
    start_time = time.time()
    start_timer()
    pin.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A0_callback)

# CUENTA pieza y resetea T.Act
def GPIO_A1_callback(pin):
    pin.irq(handler=None)
    print("GPIO_A1_callback Falling edge detected for: ", pin)
    global on_time_pz
    on_time_pz += 1
    pin.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A1_callback)

# RESET GENERAL
# Resetea contador de piezas
# Resetea contador de piezas en retraso
def GPIO_A2_callback(pin):
    pin.irq(handler=None)
    print("GPIO_A2_callback Falling edge detected for: ", pin)
    on_time_pz = 0
    delayed_pz = 0
    pin.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A2_callback)

# Can an interrupt be interrupted?
def setup_gpios():
    GPIO_A0 = Pin(26, Pin.IN, Pin.PULL_UP)
    GPIO_A1 = Pin(27, Pin.IN, Pin.PULL_UP)
    GPIO_A2 = Pin(28, Pin.IN, Pin.PULL_UP) 
    #GPIO_A0.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_FALLING)
    GPIO_A0.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A0_callback)
    GPIO_A1.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A1_callback)
    GPIO_A2.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A2_callback)

setup_display()
setup_gpios()
