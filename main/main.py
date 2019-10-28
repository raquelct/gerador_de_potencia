
from ota_updater import OTAUpdater


def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/raquelct/gerador_de_potencia.git')
    o.download_and_install_update_if_available('raquel', '244466666')

def calculate_time(pot):
    time_ms = (1.25*3600000)/pot
    return time_ms


def start():
    import ble
    import led

    calc_time = calculate_time(1000)

    while(1):
        if ble.mensage_received:
            ble.mensage_received = False
            try:
                calc_time = calculate_time(int(ble.mensage))
            except ValueError as e:
                print("Error converting value")
            
        led.blink(80, calc_time)


def boot():
    download_and_install_update_if_available()
    start()


boot()