#!/usr/bin/python3
# SNDINFO generator v3
 
import sys
import os
 
def main(pk3root, allow_lumpnames, allow_fullpaths):
    used_soundnames = {}
    randomized = {}
    warning = False
    
    def add_entry(name, filepath, randomize=True):
        if name in used_soundnames:
            print('WARNING: conflicting sound names: {} {}'.format(used_soundnames[name], filepath))
            warning = True
            return
   
        used_soundnames[name] = filepath
        sndinfo.write(name + ' "' + filepath + '"' + '\n')
        
        if randomize:
            number = ''
            while name[-1].isdigit():
                number += name[-1]
                name = name[:-1]
            if number:   
                if name in randomized:
                    randomized[name].append(number)
                else:
                    randomized[name] = [number]
        
    with open(os.path.join(pk3root, 'sndinfo.sux'), 'w') as sndinfo:
        sndinfo.write('DSEMPTY DSEMPTY\n')
        sndinfo.write('NOSOUND DSEMPTY\n')
    
        os.chdir(pk3root)
        for root, dirs, files in os.walk('sounds', onerror=raise_error):
            for file in files:
                root = root.replace('\\', '/').lower()
                filepath = root + '/' + file
                lumpname = os.path.splitext(file)[0].upper()
                if root[7:] == '':
                    filepath_sndinfoname = lumpname
                else:
                    filepath_sndinfoname = root[7:] + '/' + lumpname
                
                                
                if allow_lumpnames:
                    add_entry(lumpname, filepath) 
                if allow_fullpaths and lumpname != filepath_sndinfoname:
                    add_entry(filepath_sndinfoname, filepath)
                        
        for name, digits in randomized.items():
            if len(digits) < 2:
                continue
            if name in used_soundnames:
                print('WARNING: existing sound {} overrides the randomized sound set with the same name'.format(name))
                warning = True
                continue
                
            sndinfo.write('$random ' + name + ' { ')
            for digit in digits:
                sndinfo.write(name + digit + ' ')
            sndinfo.write('} \n')
        
    sys.exit(int(warning))
 
def raise_error(x):
    raise x
 

USAGE = """Usage: sndinfogen <pk3 root> [mode]

Mode can be one of the following:
lumpnames - enables referring to sounds by lump names only (default)
fullpaths - enables referring to sounds by full paths only
both      - sounds can be referred to by both full paths and lump names
"""

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(USAGE)
        sys.exit(2)
    
    pk3root = sys.argv[1]
    if len(sys.argv) == 3:
        mode = sys.argv[2]
    else:
        mode = 'lumpnames'
    
    if mode == 'lumpnames':
        main(pk3root, allow_lumpnames=True, allow_fullpaths=False)
    elif mode == 'fullpaths':
        main(pk3root, allow_lumpnames=False, allow_fullpaths=True)
    elif mode == 'both':
        main(pk3root, allow_lumpnames=True, allow_fullpaths=True)
    else:
        print('Unknown mode:', mode)
        sys.exit(2)
