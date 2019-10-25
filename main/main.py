
from ota_update.main.ota_updater import OTAUpdater


def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/raquelct/gerador_de_potencia.git')
    o.download_and_install_update_if_available('LAPADA', '244466666')


def start():
    # your custom code goes here. Something like this: ...
    # from main.x import YourProject
    # project = YourProject()
    # ...
    import ble


def boot():
    download_and_install_update_if_available()
    start()


boot()