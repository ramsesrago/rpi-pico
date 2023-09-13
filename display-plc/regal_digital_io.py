import time
import board
import countio
from digitalio import DigitalInOut, Direction, Pull
import asyncio
import keypad
import time
import rgbmatrix
import hub75

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=3,
    rgb_pins=[board.R0, board.G0, board.B0, board.R1, board.G1, board.B1],
    addr_pins=[board.ROW_A, board.ROW_B, board.ROW_C, board.ROW_D],
    clock_pin=board.CLK, latch_pin=board.LAT, output_enable_pin=board.OE)



#GPIO_A0 = DigitalInOut(board.A0)
#GPIO_A0.direction = Direction.INPUT

async def GPIO_A0_callback(pin):
    """Print a message when pin goes low."""
    with keypad.Keys((pin,), value_when_pressed=False, pull=True) as keys:
        while True:
            if event := keys.events.get():
                if event.pressed:
                    print(f"A0 callback !")
            await asyncio.sleep(0)
            
async def GPIO_A1_callback(pin):
    """Print a message when pin goes low."""
    with keypad.Keys((pin,), value_when_pressed=False, pull=True) as keys:
        while True:
            if event := keys.events.get():
                if event.pressed:
                    print(f"A1 callback !")
            await asyncio.sleep(0)

async def main():
    GPIO_A0_interrupt = asyncio.create_task(GPIO_A0_callback(board.A0))
    GPIO_A1_interrupt = asyncio.create_task(GPIO_A1_callback(board.A1))
    await asyncio.gather(GPIO_A0_interrupt)
    await asyncio.gather(GPIO_A1_callback)
    
asyncio.run(main())