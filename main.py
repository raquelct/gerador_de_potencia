#import network
#import uftpd
import time
from machine import Pin
import ble

# def do_connect():
#     ap = network.WLAN(network.AP_IF) # create access-point interface
#     ap.config(essid='ESP-AP-MEDIDOR') # set the ESSID of the access point
#     ap.active(True)         # activate the interface
#     print('network config:', ap.ifconfig())

def read_file(file_name):
    file = open(file_name, "r")
    str = file.read()
    file.close()
    return str

def write_file(file_name, data):
    file = open(file_name, "w")
    file.write(data)
    file.close()

led = Pin(5, Pin.OUT, value=0)
pot = int(read_file("pot.txt"))
previous_ms = 0
interval = 10
watts_second = 0
counter = 0
#do_connect()

while True: 
    if ble.mensage_received:
        ble.mensage_received = False
        try:
            pot = (int(ble.mensage))
            write_file("pot.txt", ble.mensage)
        except ValueError as e:
            print("Error converting value")

    current_ms = time.ticks_ms() 
    if (watts_second >= 4500):
        watts_second = watts_second - 4500
        counter = 0
        led.value(1)
        print("led on")
    if (time.ticks_diff(current_ms, previous_ms) >= interval):
        previous_ms = current_ms 
        watts_second = watts_second + (pot * (interval/1000))
        counter = counter + 1
    if (counter == (80/interval) and led.value() == 1):
        led.value(0)
        print("led off")


    
