#!/usr/bin/python3
 
import sys
import os
 
def main():
    if len(sys.argv) != 2:
        print('Usage: sndinfogen <pk3 root>')
        sys.exit(2)
 
    pk3root = sys.argv[1]
 
    sounds = {}
    with open(os.path.join(pk3root, 'sndinfo.sux'), 'w') as sndinfo:
        for root, dirs, files in os.walk(os.path.join(pk3root, 'sounds'), onerror=raise_error):
            for file in files:
                filepath = os.path.join(root, file)
                lumpname = os.path.splitext(file)[0].upper()
                if lumpname in sounds:
                    print('WARNING: conflicting sounds names: {} {}'.format(sounds[lumpname], filepath))
                else:
                    sndinfo.write(lumpname + ' ' + lumpname + '\n')
                    sounds[lumpname] = filepath
 
def raise_error(x):
    raise x
 
if __name__ == '__main__':
    main()
	