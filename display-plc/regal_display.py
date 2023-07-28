from interstate75 import Interstate75
from picographics import PicoGraphics

display = PicoGraphics(display=Interstate75.DISPLAY_INTERSTATE75_64X32)

#display.clear()

display.set_font("bitmap8")
display.set_backlight(0.5)
display.set_thickness(1)
display.set_pen(10)  # White

display.clear()

#display.text("Hello World", 1, 1, scale=1)
display.text("Hello World", 1, 1, scale=2)
display.set_font("bitmap8")
display.character(38, 0, 0, scale=2)

display.update()