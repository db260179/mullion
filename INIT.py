# Thanks to zecoxao and flatz <3

import struct
from binascii import unhexlify as uhx
from binascii import hexlify as hx
from Crypto.Cipher import AES
from Crypto.Hash import SHA, HMAC, CMAC

import os
import sys

EID1KEYS = [
'88228B0F92C4C36AF097F1FE948D27CE',
'5794BC8C2131B1E3E7EC61EF14C32EB5', 
]

INITKEYS = [
'48FF6BFA9C172C6E14AE444419CAF676'
]

ZEROS128 =   ['00000000000000000000000000000000']

def aes_decrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(input)
    
def aes_decrypt_ecb(key, input):
    return AES.new(key, AES.MODE_ECB).decrypt(input)
    
def aes_encrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(input)

def main(argc, argv):
        with open(sys.argv[1], 'rb') as f:
            data = f.read()
            data1 = data[0x2A0:0x2B0]
            data2 = data[0x2B0:0x2C0]
            data3 = data[0x2C0:0x2D0]
            data4 = data[0x2D0:0x2E0]
            data5 = data[0x2E0:0x300]
            data6 = data[0x300:0x320]
            data7 = data[0x320:0x340]
            data8 = data[0x340:0x360]
            eid1 = data[0x10:0x290]
            hash = data[0x290:0x2A0]
            cmac1= CMAC.new(uhx(EID1KEYS[0]), ciphermod=AES)
            cmac1.update(eid1)
            print(hx(hash))
            print(cmac1.hexdigest())
            sexy = aes_decrypt_cbc(uhx(EID1KEYS[0]), uhx(ZEROS128[0]), eid1)
            keyseed = sexy[:0x10]
            pck1 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), keyseed)
            pck2 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck1)
            pck3 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck2)
            pck4 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck3)
            pck5 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck4)
            pck6 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck5)
            pck7 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck6)
            pck8 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck7)
            pck9 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck8)
            pck10 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck9)
            pck11 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck10)
            pck12 = aes_encrypt_cbc(uhx(INITKEYS[0]), uhx(ZEROS128[0]), pck11)
            data1_stage1 = aes_decrypt_ecb(pck1,data1)
            data2_stage1 = aes_decrypt_ecb(pck2,data2)
            data3_stage1 = aes_decrypt_ecb(pck3,data3)
            data4_stage1 = aes_decrypt_ecb(pck4,data4)
            
            hash1 = data5[0x10:]
            body1 = data5[:0x10]
            cmac1= CMAC.new(pck1, ciphermod=AES)
            cmac1.update(body1)
            print(hx(hash1))
            print(cmac1.hexdigest())
            
            hash2 = data6[0x10:]
            body2 = data6[:0x10]
            cmac1= CMAC.new(pck1, ciphermod=AES)
            cmac1.update(body2)
            print(hx(hash2))
            print(cmac1.hexdigest())
            
            hash3 = data7[0x10:]
            body3 = data7[:0x10]
            cmac1= CMAC.new(pck1, ciphermod=AES)
            cmac1.update(body3)
            print(hx(hash3))
            print(cmac1.hexdigest())
            
            hash4 = data8[0x10:]
            body4 = data8[:0x10]
            cmac1= CMAC.new(pck1, ciphermod=AES)
            cmac1.update(body4)
            print(hx(hash4))
            print(cmac1.hexdigest())
            
            data5_stage1 = aes_decrypt_ecb(pck1,body1)
            data6_stage1 = aes_decrypt_ecb(pck1,body2)
            data7_stage1 = aes_decrypt_ecb(pck1,body3)
            data8_stage1 = aes_decrypt_ecb(pck1,body4)
            
            
            
            with open(sys.argv[1] + '.eid1.dec.bin', 'wb') as g:
                g.write(sexy)
                
            with open(sys.argv[1] + '.init.dec.bin', 'wb') as g:
                g.write(data1_stage1+data2_stage1+data3_stage1+data4_stage1+data5_stage1+data6_stage1+data7_stage1+data8_stage1)
            
            

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)