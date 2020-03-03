# SocraticBliss (R)
# Thanks to zecoxao and flatz 

from binascii import unhexlify as uhx
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

import os
import sys

CIPHERKEYS = ['160374F159B744C97F2CF2DD3EEE599D'] # FULL
CMACKEYS = ['3E0020AEF88FF50D693B6521E2A1C4F3']
ZEROS = ['00000000000000000000000000000000']

def aes_decrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(input)

def main(argc, argv):
        
    
        with open(sys.argv[1], 'rb') as f:
            data = f.read()
            header1 = data[0:0x14]+uhx(ZEROS[0])+data[0x24:0x40]
            header2 = data[0:0x4]+uhx(ZEROS[0])+ data[0x24:]
            cmac1= CMAC.new(uhx(CMACKEYS[0]), ciphermod=AES)
            cmac1.update(header1)
            print(cmac1.hexdigest())
            cmac2= CMAC.new(uhx(CMACKEYS[0]), ciphermod=AES)
            cmac2.update(header2)
            print(cmac2.hexdigest())            
            data = aes_decrypt_cbc(uhx(CIPHERKEYS[0]), data[0x30:0x40], data[0x40:])
            with open(sys.argv[1] + '.bin', 'wb') as f:
                f.write(data)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)