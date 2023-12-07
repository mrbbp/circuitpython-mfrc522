# circuitpython-RC522
CircuitPython class to access the MFRC522 RFID reader

<small>Based on the [wendlers/micropython-mfrc522](https://github.com/wendlers/micropython-mfrc522) MicroPython library.

Basic class to access RFID readers of the type [MFRC522](http://www.nxp.com/documents/data_sheet/MFRC522.pdf).
This is basically a re-write of [this](https://github.com/mxgxw/MFRC522-python) Python port for the MFRC522. I
tried to strip things down and make them more "pythonic" so the result is small enough to run on
[CircuitPython](https://github.com/adafruit/circuitpython) boards.

## Usage

Put the modules ``mfrc522.py``, ``examples/read.py``, ``examples/write.py`` to the root of the flash FS on your board.

I used the following pins for my setup:

| Signal    | GPIO RP2040 XIAO | Note                                 |
| --------- | ---------------- | ------------------------------------ |
| sck       | D8               |                                      |
| mosi      | D10              |                                      |
| miso      | D9               |                                      |
| rst       | D6               |                                      |
| cs        | D7               |Labeled SDA on most RFID-RC522 boards |

Now enter the REPL you could run one of the two examples:

For detecting, authenticating and reading from a card:

    import read
    read.do_read()

This will wait for a MifareClassic 1k card. As soon the card is detected, it is authenticated, and
16 bytes are read from address 0x08.

For detecting, authenticating and writing to a card:

    import write
    write.do_write()

This will wait for a MifareClassic 1k card. As soon the card is detected, it is authenticated, and
16 bytes written to address 0x08.
