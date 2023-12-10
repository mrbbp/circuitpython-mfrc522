from os import uname
import mfrc522
import board
import time
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode_mac_fr import Keycode

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

keycodes = [Keycode.ZERO,
             Keycode.ONE,
             Keycode.TWO,
             Keycode.THREE,
             Keycode.FOUR,
             Keycode.FIVE,
             Keycode.SIX,
             Keycode.SEVEN,
             Keycode.EIGHT,
             Keycode.NINE,
             Keycode.COMMA
             ]

def tag_read():
  if uname()[0] == 'rp2040':
    # rdr = mfrc522.MFRC522(sck=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.D9, rst=board.D8)
    rdr = mfrc522.MFRC522(sck=board.SCK, mosi=board.MOSI, miso=board.MISO, cs=board.D7, rst=board.D6)
  else:
    raise RuntimeError("Unsupported platform")

  print("")
  print("Placez une carte sur le lecteur")
  print("")

  try:
    while True:
      (stat, tag_type) = rdr.request(rdr.REQIDL)

      if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
          led.value = False
          print("Nouveau tag détecté")
          print("  - type de tag : 0x%02x" % tag_type)
          print("  - uuid   : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
          print("")
          # récuperation de l'uuid du tag
          for i in range(4):
            for n in str(raw_uid[i]):
                # f"{num:03d}"
                # print(keycodes[int(n,16)])
                keyboard.press(keycodes[int(n,16)])
            keyboard.press(Keycode.COMMA)
            keyboard.release_all()
          #print(Keycode.ENTER)
          keyboard.press(Keycode.ENTER)
          keyboard.release_all()
          time.sleep(.005)
          print("envoie en clavier de l'uuid :",raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
          if rdr.select_tag(raw_uid) != rdr.OK:
            print("sélection erronée du tag")
          led.value = True
          time.sleep(5)
          
  except KeyboardInterrupt:
      print("Aurevoir")

tag_read()
