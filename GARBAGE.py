# Thanks to zecoxao and flatz <3

import struct
from binascii import unhexlify as uhx
from binascii import hexlify as hx
from Crypto.Cipher import AES
from Crypto.Hash import SHA, HMAC, CMAC

import os
import sys



GARBAGEKEY =   ['C8979F5726F6A130CB9309A2F7AA0C84']
FFS128 =       ['FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF']
ZEROS128 =     ['00000000000000000000000000000000']

def aes_decrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(input)
    
def aes_decrypt_ecb(key, input):
    return AES.new(key, AES.MODE_ECB).decrypt(input)
    
def aes_encrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(input)

def main(argc, argv):
        pck1 = aes_encrypt_cbc(uhx(GARBAGEKEY[0]), uhx(ZEROS128[0]), uhx(FFS128[0]))
        for x in range(0, 78, 1):
            pck1 = aes_encrypt_cbc(uhx(GARBAGEKEY[0]), uhx(ZEROS128[0]), pck1)
            print(hx(pck1))

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)