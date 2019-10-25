import bluetooth
import time
from micropython import const

_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)
_IRQ_GATTS_WRITE                     = const(1 << 2)
_IRQ_GATTS_READ_REQUEST              = const(1 << 3)
_IRQ_SCAN_RESULT                     = const(1 << 4)
_IRQ_SCAN_COMPLETE                   = const(1 << 5)
_IRQ_PERIPHERAL_CONNECT              = const(1 << 6)
_IRQ_PERIPHERAL_DISCONNECT           = const(1 << 7)
_IRQ_GATTC_SERVICE_RESULT            = const(1 << 8)
_IRQ_GATTC_CHARACTERISTIC_RESULT     = const(1 << 9)
_IRQ_GATTC_DESCRIPTOR_RESULT         = const(1 << 10)
_IRQ_GATTC_READ_RESULT               = const(1 << 11)
_IRQ_GATTC_WRITE_STATUS              = const(1 << 12)
_IRQ_GATTC_NOTIFY                    = const(1 << 13)
_IRQ_GATTC_INDICATE                  = const(1 << 14)

ble = bluetooth.BLE()
ble.active(True)

connected = False

UART_SERVICE = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ|bluetooth.FLAG_NOTIFY,)
UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,)

((tx, rx),) = ble.gatts_register_services(((UART_SERVICE, (UART_TX, UART_RX,),),))
ble.gap_advertise(100, b'\x02\x01\x02\x0C\x09MicroPython')

def bt_irq(event, data):
    global connected
    print(event, data)
    if event == _IRQ_CENTRAL_CONNECT:
        # A central has connected to this peripheral.
        conn_handle, addr_type, addr = data
        time.sleep(1)
        ble.gatts_notify(conn_handle, tx, 'Ola')	
        connected = True
    elif event == _IRQ_CENTRAL_DISCONNECT:
        # A central has disconnected from this peripheral.
        conn_handle, addr_type, addr = data
        connected = False
    elif event == _IRQ_GATTS_WRITE:
        # A central has written to this characteristic or descriptor.
        conn_handle, attr_handle = data
        msg = ble.gatts_read(rx).decode()
        print(msg)
    elif event == _IRQ_GATTS_READ_REQUEST:
        # A central has issued a read. Note: this is a hard IRQ.
        # Return None to deny the read.
        conn_handle, attr_handle = data

ble.irq(bt_irq)
