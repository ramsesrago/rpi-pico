import machine
import time

pin = machine.Pin(25, machine.Pin.IN)  # Use any available GPIO pin number
start = time.ticks_us()
value = pin.value()
end = time.ticks_us()

print("Elapsed time:", end - start, "us")