import usb_midi
import adafruit_midi  # MIDI protocol encoder/decoder library
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from os import uname
import mfrc522
import board
import time
from os import uname
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

def do_read():

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
          print("  - uid   : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
          print("")
          # récuperation de l'uuid du tag
          for i in range(4):
            # formate la valeur en 2 x 7bits pour le midi 
            data2 = raw_uid[i] >> 7
            data1 = raw_uid[i] & 0x7F
            # envoie en midi
            usb_midi.send(ControlChange(i*2, data2))
            usb_midi.send(ControlChange((i*2)+1, data1))
            time.sleep(.005)

          if rdr.select_tag(raw_uid) != rdr.OK:

#             key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
# 
#             if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
#               print("Address 8 data: %s" % rdr.read(8))
#               rdr.stop_crypto1()
#             else:
#               print("Pas d'Authentication")
            print("sélection erronée du tag")
            
          #time.sleep(.5)
          led.value = True
          time.sleep(5)
          
  except KeyboardInterrupt:
      print("Aurevoir")



global tag
# init du midi
USB_MIDI_channel = 1  # pick your USB MIDI out channel here, 1-16

usb_midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=USB_MIDI_channel - 1,
    midi_out=usb_midi.ports[1], out_channel=USB_MIDI_channel - 1
)

print(uname())
# import write

# input_bytes = b"\x00\x0F"
# output_numbers = list(input_bytes)
# print(output_numbers)

#print(bytes([0xf,0xe,0xd,0xc,0xb,0xa,9,8,7,6,5,4,3,2,1,0]))

#write.do_write(0xABCDEF9876543210)

# import read
do_read()
