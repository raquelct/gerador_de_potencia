import network
import ble
import led
import uftpd

def do_connect():
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.config(essid='ESP-AP-MEDIDOR') # set the ESSID of the access point
    ap.active(True)         # activate the interface
    print('network config:', ap.ifconfig())

def calculate_time(pot):
    time_ms = (1.25*3600000)/pot
    return time_ms

calc_time = calculate_time(1000)
do_connect()

while(1):
    if ble.mensage_received:
        ble.mensage_received = False
        try:
            calc_time = calculate_time(int(ble.mensage))
        except ValueError as e:
            print("Error converting value")
        
    led.blink(80, calc_time)  
