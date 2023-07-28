# '''
# buttons.py
# Push either switch A, switch B or the BOOT switch (in the case of the non-w version) to change the display
# '''
# import interstate75
# 
# i75 = interstate75.Interstate75(display=interstate75.DISPLAY_INTERSTATE75_64X32)
# graphics = i75.display
# 
# width = i75.width
# height = i75.height
# 
# A_COLOR = graphics.create_pen(0x31, 0x81, 0xCE)
# A_TEXT = graphics.create_pen(0xCE, 0x7E, 0x31)
# 
# BOOT_COLOR = graphics.create_pen(0xC3, 0x3C, 0xBD)
# BOOT_TEXT = graphics.create_pen(0x3C, 0xC3, 0x42)
# 
# BG = graphics.create_pen(0xC1, 0x99, 0x3E)
# 
# 
# def display_a():
#     graphics.set_pen(A_COLOR)
#     graphics.clear()
#     graphics.set_pen(A_TEXT)
#     graphics.text("T. Est", 8, 6, False, 3)
#     i75.update()
# 
# 
# def display_boot():
#     graphics.set_pen(BOOT_COLOR)
#     graphics.clear()
#     graphics.set_pen(BOOT_TEXT)
#     graphics.text("BOOT", 5, 11, False, 1)
#     i75.update()
# 
# 
# graphics.set_pen(BG)
# graphics.clear()
# i75.update()
# 
# while 1:
#     if i75.switch_pressed(interstate75.SWITCH_A):
#         display_a()
#     if i75.switch_pressed(interstate75.SWITCH_BOOT):
#         display_boot()
# 
#

from interstate75 import Interstate75
import time
from machine import Pin, Timer
import _thread

# Display definitions
i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
graphics = i75.display
MAGENTA = graphics.create_pen(255, 0, 255)
BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)
GREEN = graphics.create_pen(34, 139, 34)
RED = graphics.create_pen(255, 0, 0)

# Timer definitions
total_time = 100

# PLC definitions
delayed_pz = 10

def setup_display():
    graphics.clear()
    graphics.set_font("bitmap8")
    graphics.set_thickness(25)
    
def display_actual_time(formatted_time):
    graphics.set_pen(BLACK)
    graphics.clear()
    graphics.set_pen(GREEN)
    graphics.text("T.Act: ", 1, 15, scale=1)
    graphics.text(formatted_time, 1, 22, scale=1)
    
def display_est_time():
    graphics.set_pen(WHITE)
    graphics.text("T.Est", 1, 0, scale=1)
    graphics.text("01:05", 1, 6, scale=1)

def display_curr_count():
    graphics.set_pen(MAGENTA)
    graphics.text("C:398", 32, 0, scale=1)

def display_delayed_pz():
    # Imprimir cuenta de piezas retrasadas
    # Se incrementa cuando se detecta que sale una pieza
    # y el T.Act > T.Est
    graphics.set_pen(RED)
    delayed_pz_str = str(delayed_pz)
    graphics.text(delayed_pz_str, 32, 16, scale=2)

def time_tick(timer):
    global time_left, start_time, total_time
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

setup_display()
# Start timer
global start_time
start_time = time.time()
start_timer()
