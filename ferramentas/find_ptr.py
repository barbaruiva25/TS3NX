"""Acha ponteiros (dword big-endian) para um endereco guest dentro da imagem do
Sims3.xex, com o contexto de 4 dwords em volta (vtable/callback table). Saida
para uso como evidencia de uma entrada do overrides.toml.

Uso: python ferramentas/find_ptr.py 0x8907D040
"""
import struct
import sys

IMG_PATH = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\LOGS\sims3_image.bin'
BASE = 0x88000000


def main():
    addr = int(sys.argv[1], 16)
    d = open(IMG_PATH, 'rb').read()
    needle = struct.pack('>I', addr)
    hits = []
    start = 0
    while True:
        i = d.find(needle, start)
        if i < 0:
            break
        hits.append(BASE + i)
        start = i + 1
    print('ponteiros para %08X: %d' % (addr, len(hits)))
    for h in hits[:12]:
        off = h - BASE
        print('  em %08X' % h)
        for k in range(-4, 5):
            v = struct.unpack_from('>I', d, off + 4 * k)[0]
            tag = '  <== alvo' if k == 0 else ''
            print('    %+3d: %08X%s' % (k, v, tag))


if __name__ == '__main__':
    main()