# python2
import sys
import struct

def hexdump(src, length=16, sep='.', start=0):
  # based on https://gist.github.com/7h3rAm/5603718
  FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
  lines = []
  for c in range(0, len(src), length):
    chars = src[c:c+length]
    hexstr = ' '.join(["%02X" % ord(x) for x in chars]) if type(chars) is str else ' '.join(['{:02X}'.format(x) for x in chars])
    if len(hexstr) > 24:
      hexstr = "%s %s" % (hexstr[:24], hexstr[24:])
    printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars]) if type(chars) is str else ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])
    lines.append("%08X:  %-*s  |%s|" % (start, length*3, hexstr, printable))
    start += length
  return '\n'.join(lines)


def parse_patch(paddress, pdata, pcodeaddress):
  ret = ""
  address = struct.unpack('<I', paddress)[0]
  if address >= 0x60000-4:
    ret += "-------    --------    ";
  else:
    ret += "0x{:05X}    {:08X}    ".format(address, struct.unpack('>I', pdata)[0])
  codeaddress = struct.unpack('<I', pcodeaddress)[0]
  if codeaddress < 0x2000000 or codeaddress >= 0x2010000-2:
    ret += "---------";
  else:
    ret += "0x{:07X}".format(codeaddress)
  return ret


def parse_hdmi_patch(paddress, pselect):
    ret = ""
    address = struct.unpack('<' + 'I'*25, paddress)[::-1]
    select = struct.unpack('<I', pselect)[0]
    if select == 0:
        print "non selected!"
    j = 0
    for i in xrange(0, 25):
        if select & (1 << i):
            print "{:02}                         0x{:07X}".format(i+1, address[j])
            j += 1
    print ""


def main(argc, argv):
  with open(sys.argv[1], 'rb') as f:
      patch = f.read()
      print "Firmware Version: {}.{}       Patch Version: {}.{}".format(struct.unpack('<H', patch[0:2])[0], struct.unpack('<H', patch[2:4])[0], struct.unpack('<H', patch[4:6])[0], struct.unpack('<H', patch[6:8])[0])
      print ""
      print "                  Offset     Data/Instr  Code Offset"
      print "Patch 0:          " + parse_patch(patch[0x08:0x0C], patch[0x18:0x1C], patch[0x28:0x2C])
      print "Patch 1:          " + parse_patch(patch[0x0C:0x10], patch[0x1C:0x20], patch[0x2C:0x30])
      print "Patch 2:          " + parse_patch(patch[0x10:0x14], patch[0x20:0x24], patch[0x30:0x34])
      print "Patch 3:          " + parse_patch(patch[0x14:0x18], patch[0x24:0x28], patch[0x34:0x38])
      print ""
      print "Code:"
      print hexdump("\x00"*8 + patch[0x38:0x3C0], 16, '.', 0x200F070)
      print ""
      print ""
      print "HDMI State Function        Code Offset"      
      parse_hdmi_patch(patch[0xF54:0xFB8], patch[0xFB8:0xFBC])
      print ""
      print "HDMI Code:"
      print hexdump(patch[0x3C0:0xF54], 16, '.', 0x200F400)
      print ""
      print "HDMI Checksum: 0x{:04X}".format(struct.unpack('<H', patch[0xFBE:0xFC0])[0])

if __name__ == '__main__':
  main(len(sys.argv), sys.argv)