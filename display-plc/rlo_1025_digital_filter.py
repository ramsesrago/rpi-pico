# '''
# regal.py

from interstate75 import Interstate75
import time
from machine import Pin, Timer
import _thread
import regal_font

lock = _thread.allocate_lock()  # Lock for synchronization

# Display definitions
i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
graphics = i75.display
i75.set_led(0, 255, 0)
MAGENTA = graphics.create_pen(255, 0, 255)
BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)
GREEN = graphics.create_pen(57, 255, 20)
RED = graphics.create_pen(255, 24, 24)
BLUE = graphics.create_pen(8, 51, 162)
graphics.set_backlight(1)

## This variable is used to change "T.Est"
est_time = time.localtime(110) 
est_formatted_time = "{a:02d} :{b:02d}".format(a = est_time[4], b = est_time[5]%60)
elapsed_time = 0

# Dictionary to capture the timestamp of the last interrupt
last_interrupt_times = {}
debounce_delay = 80  # Adjust this value to your debounce requirements (in milliseconds)

# Performance metrics
gpio_0_interrupt_count = 0
gpio_1_interrupt_count = 0
gpio_2_interrupt_count = 0

gpio_a0_state = 1
gpio_a1_state = 1
gpio_a2_state = 1
gpio_a0_irq_flags = 0
gpio_a1_irq_flags = 0
gpio_a2_irq_flags = 0

start_time = 0
# PLC definitions
## A0
## INICIO ciclo (START)
## A1
## CUENTA pieza (PARO), (STOP)
## A2
## RESET general, GENERAL RESET
delayed_pz = 0
on_time_pz = 0

# State enumeration
class States:
    IDLE = 0
    GPIO_A0_TRIGGERED = 1
    GPIO_A1_TRIGGERED = 2
    GPIO_A2_TRIGGERED = 3

# State variable
state = States.IDLE

class InterruptEvent:
    def __init__(self, event_type, event_pin, event_data=None):
        self.event_type = event_type
        self.event_pin = event_pin
        self.event_data = event_data
        
class gpio_interrupt_queue:
    def __init__(self, size=100):
        self.queue = []
        self.size = size

    def enqueue(self, event):
        if len(self.queue) >= self.size:
            # Handle queue overflow, like removing the oldest event
            self.queue.pop(0)
        self.queue.append(event)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0



def setup_display():
    global my_font
    graphics.clear()
    graphics.set_font(regal_font.font)
    graphics.set_thickness(2)
    graphics.set_pen(BLACK)
    graphics.clear()
    display_actual_time("00 :00")
    display_est_time()
    display_curr_count()
    display_delayed_pz()
    i75.update(graphics)
    
def display_actual_time(formatted_time):
    graphics.set_pen(GREEN)
    graphics.text("T.Act", 0, 16, scale=1)
    graphics.text(formatted_time, 0, 24, spacing = 1, scale=1)
    
def display_est_time():
    graphics.set_pen(WHITE)
    graphics.text("T.Est", 0, 0, scale=1)
    graphics.text(est_formatted_time, 0, 8, spacing = 1, scale=1)

def display_curr_count():
    graphics.set_pen(MAGENTA)
    graphics.text("C:" + str(on_time_pz), 32, 4, spacing = 1, scale=1)

# Prints delayed piece counter
# Incremented when a piece is detected
def display_delayed_pz():    
    graphics.set_pen(RED)
    delayed_pz_str = str(delayed_pz)
    graphics.text(delayed_pz_str, 30, 16, scale=2)

def time_tick(timer):
    global start_time, elapsed_time
    # using the time() function will likely be more accurate than counting the ticks, plus we can mess with the tick frequency now.
    current_time = time.time()
    elapsed_time = current_time - start_time
    
def update_display_callback(timer):
    global formatted_time, elapsed_time
    formatted_time = "{a:02d} :{b:02d}".format(a = elapsed_time//60, b = elapsed_time%60)
    graphics.set_pen(BLACK)
    graphics.clear()
    display_actual_time(formatted_time)
    display_est_time()
    display_curr_count()
    display_delayed_pz()
    i75.update(graphics)
    
def setup_timers():
    global tick_timer, update_display_timer
    tick_timer = Timer(period=86400000, mode=Timer.ONE_SHOT, callback=time_tick)
    update_display_timer = Timer(period=500, mode=Timer.PERIODIC, callback=update_display_callback)    
    
def debounce_interrupt(pin):
    
    global last_interrupt_times
    
    with lock:  # Acquire the lock before accessing shared data
        current_time = time.ticks_ms()
        last_interrupt_time = last_interrupt_times.get(pin, 0) # Default value is 0

         # Check if enough time has elapsed since the last interrupt
        if time.ticks_diff(current_time, last_interrupt_time) >= debounce_delay:
            #print("Valid interrupt for pin: ", pin)
            last_interrupt_times[pin] = current_time
            print("FALLING edge for pin: ", pin)
            return True
                
    return False

# INICIO empieza timer
def GPIO_A0_callback(pin):
    #pin.irq(handler=None)
    global state, gpio_interrupt_queue
    if (debounce_interrupt(pin)):
        event = InterruptEvent(event_type=States.GPIO_A0_TRIGGERED, event_pin=pin, event_data=time.ticks_us())
        gpio_interrupt_queue.enqueue(event)
    

# CUENTA pieza y resetea T.Act
#### CONDICION 1
# Si el tiempo de la pieza contada excedio el T.est
# Se tiene que incrementar el contador de piezas retrasadas (delayed_pz)
# Ademas se incrementa el contador de piezas a  timepo (on_time_pz)
# Se incrementa el ROJO y el MAGENTA

#### CONDICION 2
# Si el tiempo de la pieza contada esta dentro del T.est
# Se incrementa el contador de piezas a tiempo (on_time_pz)
# Se incrementa el MAGENTA

def GPIO_A1_callback(pin):
    global state, gpio_interrupt_queue
    if (debounce_interrupt(pin)):
        event = InterruptEvent(event_type=States.GPIO_A1_TRIGGERED, event_pin=pin, event_data=time.ticks_us())
        gpio_interrupt_queue.enqueue(event)
            

# GENERAL RESET
# Reset piece counter
# Reset delayed piece counter
def GPIO_A2_callback(pin):
    global state, gpio_interrupt_queue
    if (debounce_interrupt(pin)):
        event = InterruptEvent(event_type=States.GPIO_A2_TRIGGERED, event_pin=pin, event_data=time.ticks_us())
        gpio_interrupt_queue.enqueue(event)
    
# MOVING AVERAGE FILTER
def filter_gpio(pin):
    N = 200  # Number of readings to keep for averaging
    readings = [0] * N  # Initialize list with N zeros
    reading_index = 0
    start = time.ticks_us()
    for i in range(N):
        readings[i] = pin.value()
        
    end = time.ticks_us()
    elapsed_time_us = end - start
    print(f"Function took {elapsed_time_us} us to run.")
    gpio_zeroes_count = readings.count(0)
    
    return 100 * (gpio_zeroes_count / len(readings))

        
# State handlers
def handle_GPIO_A0(pin):
    print("handle_GPIO_A0")
    average = filter_gpio(pin)
    print("Average: ", average)
    if (average > 90):
        global start_time, elapsed_time, formatted_time, gpio_0_interrupt_count
        gpio_0_interrupt_count += 1
        elapsed_time = 0
        formatted_time = "00 :00"
        start_time = time.time()
        tick_timer.init(period=1000, mode=Timer.PERIODIC, callback=time_tick)

def handle_GPIO_A1(pin):
    print("handle_GPIO_A1")
    average = filter_gpio(pin)
    print("Average: ", average)
    if (average > 90):
        global on_time_pz, elapsed_time, delayed_pz, tick_timer, gpio_1_interrupt_count
        gpio_1_interrupt_count += 1
        # Stops the general timer
        tick_timer.deinit()    
        total_time = est_time[5] + est_time[4]*60
        if (elapsed_time < total_time):
            on_time_pz += 1
        else:
            on_time_pz += 1
            delayed_pz += 1

def handle_GPIO_A2(pin):
    print("handle_GPIO_A2")
    average = filter_gpio(pin)
    print("Average: ", average)
    if (average > 90):
        global on_time_pz, delayed_pz, formatted_time, tick_timer, elapsed_time, gpio_2_interrupt_count
        gpio_2_interrupt_count += 1
        on_time_pz = 0
        delayed_pz = 0
        elapsed_time = 0
        formatted_time = "00 :00"
        tick_timer.deinit()
    

# Can an interrupt be interrupted?
def setup_gpios():
    global GPIO_A0, GPIO_A1, GPIO_A2, last_interrupt_times, gpio_interrupt_queue
    GPIO_A0 = Pin(26, Pin.IN, Pin.PULL_UP)
    GPIO_A1 = Pin(27, Pin.IN, Pin.PULL_UP)
    GPIO_A2 = Pin(28, Pin.IN, Pin.PULL_UP)
    # Initialize dictionary
    last_interrupt_times = {GPIO_A0: 0, GPIO_A1: 0, GPIO_A2: 0}
    GPIO_A0.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A0_callback)
    GPIO_A1.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A1_callback)
    GPIO_A2.irq(trigger=Pin.IRQ_FALLING, handler=GPIO_A2_callback)
    # interrupt queue
    gpio_interrupt_queue = gpio_interrupt_queue()


# Main loop
def main():
    global state
    
    setup_display()
    setup_timers()
    time.sleep(10)
    setup_gpios()

    while True:
        if not gpio_interrupt_queue.is_empty():
            print("queue not empty")
            event = gpio_interrupt_queue.dequeue()
            if event.event_type == States.GPIO_A0_TRIGGERED:
                handle_GPIO_A0(event.event_pin)
                state = States.IDLE  # Reset state to idle after handling
            elif event.event_type == States.GPIO_A1_TRIGGERED:
                handle_GPIO_A1(event.event_pin)
                state = States.IDLE
            elif event.event_type == States.GPIO_A2_TRIGGERED:
                handle_GPIO_A2(event.event_pin)
                state = States.IDLE
        time.sleep(0.01)  # Sleep for a bit to prevent maxing out CPU

if __name__ == "__main__":
    main()

        

