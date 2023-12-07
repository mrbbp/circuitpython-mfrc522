"""
Exemple de lecture de tag avec un module ``mfrc522``.
"""

# 3rd party
import board

# this package
import mfrc522


def do_read():
        # modified for rp2040 - XIAO
	rdr = mfrc522.MFRC522(board.SCK, board.MOSI, board.MISO, cs=board.D7, rst=board.D6)
	rdr.set_antenna_gain(0x07 << 4)

	print('')
	print("Posez un tag sur le lecteur pour lire les données")
	print('')

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("Tag détecté")
					print("  - Type de tag : 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print('')

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Données (Address 8 data) : %s" % rdr.read(8))
							rdr.stop_crypto1()
						else:
							print("Erreur d'authentication")
					else:
						print("Selection du tag éronnée")

	except KeyboardInterrupt:
		print("Au revoir")
