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

TIMEKEYS = [
'5EC26719DD05CF73E36358DEEC6EF10E',
'85BFE5F04826819F754F4B735438105B',
'767A0AA40672D75C2C57665243466FE0',
'8D904F16239C6C56D20C3AAE424B6FDF',
]

TIMESEEDS = [
'A8DCAB3577F30F7B81C788B80446B03F',
'C240BD9F72BBFC7268E4E688C1C24F6E',
'EF100F2B53199715A99C3E4794487073',
'74CE56F619FBD2486115A2FBA4F5FBB4',
]

TIMEFINALS = [
'E3EFDE987E4A2D3F8CF7B3B60E846B21',
'4AB026664E9D02F53EFF9544549B1F97',
'7ECA7F299891F1B243119E35AE94C3DE',
'E0B7A0867CF44923BAE65E3386460C80',
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
            data1 = data[0x4E0:0x500]
            data2 = data[0x500:0x520]
            data3 = data[0x520:0x540]
            data4 = data[0x540:0x560]
            eid1 = data[0x10:0x290]
            hash = data[0x290:0x2A0]
            cmac1= CMAC.new(uhx(EID1KEYS[0]), ciphermod=AES)
            cmac1.update(eid1)
            print(hx(hash))
            print(cmac1.hexdigest())
            sexy = aes_decrypt_cbc(uhx(EID1KEYS[0]), uhx(ZEROS128[0]), eid1)
            keyseed = sexy[0x150:0x160]
            pck1 = aes_encrypt_cbc(uhx(TIMEKEYS[0]), uhx(ZEROS128[0]), keyseed)
            pck2 = aes_encrypt_cbc(uhx(TIMEKEYS[1]), uhx(ZEROS128[0]), keyseed)
            pck3 = aes_encrypt_cbc(uhx(TIMEKEYS[2]), uhx(ZEROS128[0]), keyseed)
            pck4 = aes_encrypt_cbc(uhx(TIMEKEYS[3]), uhx(ZEROS128[0]), keyseed)
            data1_stage1 = aes_decrypt_ecb(pck1,data1)
            data1_body = data1_stage1[:0x10]
            data1_stage2 = aes_decrypt_ecb(uhx(TIMEFINALS[0]),data1_stage1)[:0x10]
            data1_omac = data1_stage1[0x10:]
            cmac2= CMAC.new(uhx(TIMEFINALS[0]), ciphermod=AES)
            cmac2.update(data1_body)
            print(hx(data1_omac))
            print(cmac2.hexdigest())
            
            with open(sys.argv[1] + '.eid1.dec.bin', 'wb') as g:
                g.write(sexy)
                
            with open(sys.argv[1] + '.time1.dec.bin', 'wb') as g:
                g.write(data1_stage2)
            
            

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)