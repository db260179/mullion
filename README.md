# mullion
A collection of scripts for ps3 syscon CXR(F)

## Python requirements
sudo -H pip install pycryptodome

FULL.py

Feed it DECR fws, get decrypted result and cmac verification

GARBAGE.py

Generates Garbage bytes from Sony's Garbage Key

INIT.py

Feed it EEPROM full dump, Decrypts and Generates INIT bytes

PTCH.py

Simple script that shows the reverse process, from PTCH body/cmac key to string

SNVS.py

Decrypts and stores EID1 and SNVS in two files, given EEPROM

TIME.py

Decrypts TIME related regions and stores them in a file, given EEPROM
