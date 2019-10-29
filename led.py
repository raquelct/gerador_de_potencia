from machine import Pin
import time

led = Pin(5, Pin.OUT, value=0)

def blink(time_on, time_off):
    led.value(1)
    time.sleep_ms(int(time_on))
    led.value(0)
    time.sleep_ms(int(time_off))
    print("Led is blinking at %d ms" %time_off)