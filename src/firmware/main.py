import time

from machine import Pin

led = Pin("LED", Pin.OUT)

for i in range(5):
    led.toggle()
    print("tick", i)
    time.sleep_ms(250)

led.off()
print("done")
