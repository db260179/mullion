# SocraticBliss (R)
# Thanks to zecoxao and flatz <3

from binascii import unhexlify as uhx
from binascii import hexlify as hx
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

import os
import sys

AKEYS = [
'C1D5D39BBC56839E95AB842233FF1C59', # COK-001
'C9D03C410A120F66E4F4A96ADAF5ADAA', # COK-002 / COK-002W
'D484266DB6C3AE16B1B82DDBBBF99479', # SEM-001
'0121F8AB75898AD2C58D3546B7D8F72E', # DIA-001
'6B3583DA1AA6B49106E1641178EE68C8', # DIA-002 / DEB-001
'F790F953D734AC5D7C78EE498B98CE48', # ???
'881AE6022FAEDDE0FABC01DFFABAE140', # ???
'C4AB610A03B98A9B9E52FEF972967523', # DYN-001
]

CKEYS = [
'FDFCE3EB57BAE13A39B127BB3226DA14', # COK-001
'746D66511105D0DB54BF3EDFAD275EAC', # COK-002 / COK-002W
'7843E32BA18B34355436C2F657F41F16', # SEM-001
'310068E416324779C32C47D32B39CAB5', # DIA-001
'6E9CE7C57BFC27CDD59A05093ADFE475', # DIA-002 / DEB-001
'C5E30C6393A1EE315E3F9BCA4CF275B0', # ???
'A40B57FB1BCB160F99F9F126B8477D1C', # ???
'B80A6FE26686C4F119AD76901D431494', # DYN-001
]

MASTER = '5E7CD16A78443928120688D7883493F1'
XOR1   = 'D6DD7D29B4F55B318091821CF7C84A3C'
XOR2   = '1828374D624774AF0144535DE54FF10F'
XOR3   = '0B3C10FF47FC9D3437CA80952CAE9170'
ZEROS  = '00000000000000000000000000000000'

def aes_decrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(input)
    
def aes_encrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(input)

def printem(list):
    for key in list:
        print(hx(''.join(key)))
        
def printem2(list):
    for key in list:
        print((''.join(key)))

def steps(type):
    
    print('\nFIRST STEP - DECRYPT:\n')
    DKEYS = [ aes_decrypt_cbc(uhx(MASTER), uhx(ZEROS), uhx(type[idx])) for idx, _ in enumerate(type) ]
    printem(DKEYS)
    
    print('\nSECOND STEP - XOR1:\n')
    XOR1S = [ [ chr(ord(a) ^ ord(b)) for (a,b) in zip(DKEYS[idx],  uhx(XOR1)) ] for idx, _ in enumerate(type) ]
    printem(XOR1S)
    
    print('\nTHIRD STEP - XOR3:\n')
    XOR2S = [ [ chr(ord(a) ^ ord(b)) for (a,b) in zip(XOR1S[idx], uhx(XOR3)) ] for idx, _ in enumerate(type) ]
    printem2(XOR2S)
    
def steps2(type):
    
    print('\nFIRST STEP - DECRYPT:\n')
    DKEYS = [ aes_decrypt_cbc(uhx(MASTER), uhx(ZEROS), uhx(type[idx])) for idx, _ in enumerate(type) ]
    printem(DKEYS)
    
    print('\nSECOND STEP - XOR2:\n')
    XOR1S = [ [ chr(ord(a) ^ ord(b)) for (a,b) in zip(DKEYS[idx],  uhx(XOR2)) ] for idx, _ in enumerate(type) ]
    printem(XOR1S)
    
    print('\nTHIRD STEP - XOR3:\n')
    XOR2S = [ [ chr(ord(a) ^ ord(b)) for (a,b) in zip(XOR1S[idx], uhx(XOR3)) ] for idx, _ in enumerate(type) ]
    printem2(XOR2S)

def main(argc, argv):
    
    print('\n~~~ AES ~~~')
    steps(AKEYS)
    
    print('\n~~~ CMAC ~~~')
    steps2(CKEYS)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)