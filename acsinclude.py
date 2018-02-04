#!/usr/bin/python3
 
import os
import sys
import re
import io
from sys import argv, exit
 
def readfile(filename, mode='r'):
    with open(filename, mode) as f:
        return f.read()
 
included = set()
includepath = [ '.' ]

def resolve_include(filename):
    for dir in includepath:
        filepath = os.path.join(dir, filename)
        if os.path.isfile(filepath):
            return filepath
 
    print('ERROR: {} not found in include path'.format(filename))
    exit(1)

def include_file(filename, out):
    if filename.lower() == 'zcommon.acs':
        return
   
    if filename in included:
        print('ERROR: {} included twice'.format(filename))
        exit(1)
    included.add(filename)
 
    text = readfile(resolve_include(filename))
    offset = 0
    for match in re.finditer(b'#include[ \t]+"(.*?)"', text, re.IGNORECASE):
        out.write(text[offset:match.start()])
        offset = match.end()
        include_file(match.group(1).decode('utf-8'), out)
 
    out.write(text[offset:])
 
def main(): 
    if len(argv) < 3:
        print('Usage: acsinclude <input> <output> [include directories]')
        exit(2)
 
    global includepath
    includepath = [os.path.dirname(argv[1])] + argv[3:]
 
    text = io.StringIO()
    include_file(os.path.basename(argv[1]), text)

    
    
if __name__ == '__main__':
    main()