from PIL import Image
from time import sleep
from subprocess import call
from threading import Thread
from lglcd import LogitechLcd

background_image = 'bg.png'
nircmd = 'C:/Path/nircmd.exe'
sound1 = 'TV'
sound2 = 'Speaker'
sound3 = '"My Headset"'
sound4 = 'Switch'


def load_image(sprite):
    im = Image.open(sprite)
    im = im.convert('1')
    return list(im.getdata())


def background(image):
    lcd.set_background(load_image(image))
    lcd.update()


def buttons(button):
    while process_buttons.is_alive:
        sleep(0.001)
        if lcd.is_button_pressed(button):
            if button != 8:
                sounddevice = str(button).replace('1', sound1).replace('2', sound2).replace('4', sound3)
                call(' '.join([nircmd, 'setdefaultsounddevice', sounddevice]))
                sleep(0.5)
            else:
                call(' '.join([nircmd, 'mutesysvolume 2', sound4]))
                sleep(0.5)


if __name__ == "__main__":
    lcd = LogitechLcd('Sound Device Switch')
    background(background_image)
    for button in 1, 2, 4, 8:
        process_buttons = Thread(target=buttons, args=(button, ))
        process_buttons.start()
