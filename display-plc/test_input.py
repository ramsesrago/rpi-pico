# '''
# regal.py

import time
from machine import Pin, Timer
import _thread

irq_count = 0

# INICIO empieza timer
def GPIO_A0_callback(pin):
    print("ENTRADA Falling edge detected for: ", pin)
    pin.irq(handler=None)
    global irq_count
    print("Count is: ", irq_count)
    irq_count = irq_count + 1
    print("SALIDA Falling edge detected for: ", pin)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A0_callback)

# CUENTA
def GPIO_A1_callback(pin):
    #pin.irq(handler=None)
    print("Falling edge detected for: ", pin)
    print("Pin value is: ", pin.value())
    #global on_time_pz
    #on_time_pz += 1
    # Reset timer
    pin.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A1_callback)

# RESET GENERAL
def GPIO_A2_callback(pin):
    pin.irq(handler=None)
    print("Falling edge detected for: ", pin)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A2_callback)

# Can an interrupt be interrupted?
def setup_gpios():
    print("setup_gpio")
    GPIO_A0 = Pin(26, Pin.IN, Pin.PULL_UP)
    GPIO_A1 = Pin(27, Pin.IN, Pin.PULL_UP)
    GPIO_A2 = Pin(28, Pin.IN, Pin.PULL_UP) 
    #GPIO_A0.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_FALLING)
    GPIO_A0.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A0_callback)
    GPIO_A1.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A1_callback)
    #GPIO_A1.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_FALLING)
    #GPIO_A1.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A1_callback)
    #GPIO_A1.irq(trigger=Pin.IRQ_FALLING, lambda p:print("Falling edge detected for: "))
    GPIO_A2.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A2_callback)
    print("finish")

setup_gpios()

