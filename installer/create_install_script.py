#!python3

# Run this on a Mac or Linux machine to create/update 'install_uartremote.py'
# Copy the contents of install_uartremote.py into an empty SPIKE Prime project
# And run to install

import binascii, mpy_cross, time
import hashlib
import os
from functools import partial
#MicroPython v1.14-876-gfbecba865 on 2021-05-04; LEGO Technic Large Hub with STM32F413xx
# TQUCHyCNHEgKAAcc
LIB = '../'
MPY_LIB = '../'
INSTALLER = 'install_mpy_matrix_tools.py'
BASE_SCRIPT = 'base_script.py'
SKIP_FILES = ['__pycache__', 'matrix.py']
CHUNK_SIZE = 2**8

files = [f for f in os.listdir(LIB) if f not in SKIP_FILES and ".py" in f ]
encoded = []

for f in files:
    out_file = f.split(".")[0]+".mpy"
    out_file_loc = MPY_LIB+out_file
    mpy_cross.run('-march=armv7m', LIB+f,'-o', out_file_loc)
    time.sleep(0.5)
    with open(out_file_loc,'rb') as mpy_file:
        file_hash = hashlib.sha256(mpy_file.read()).hexdigest()
    chunks = []
    with open(out_file_loc,'rb') as mpy_file:
        for chunk in iter(partial(mpy_file.read, CHUNK_SIZE), b''):
            chunks += [binascii.b2a_base64(chunk).decode('utf-8')]
    print(out_file,": ",len(chunks)," chunks of ", CHUNK_SIZE)
    encoded += [(
        out_file,
        tuple(chunks),
        file_hash
    )]


spike_code=open(BASE_SCRIPT,'r').read()

with open(INSTALLER,'w') as f:
     f.write(spike_code.format(repr(tuple(encoded))))
