"""Quem alcança um endereco guest: branches (b/bl) de dentro e de fora, e a
faixa das funcoes registradas em volta. Base para uma entrada do overrides.toml
com evidencia (nao e adivinhacao).

Uso: python ferramentas/reach.py 0x8907D040
"""
import io
import re
import struct
import sys

sys.path.insert(0, r'C:\Users\barba\Documents\xbox360\TS3NX\ferramentas')
from ppc_mini import Image, decode, text

IMG_PATH = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\LOGS\sims3_image.bin'
BASE = 0x88000000
GEN = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\generated\sims3'


def main():
    addr = int(sys.argv[1], 16)
    img = Image(IMG_PATH, BASE)
    init = io.open(GEN + r'\sims3_init.cpp', encoding='utf-8', errors='replace').read()
    pairs = sorted((int(m.group(1), 16), m.group(2)) for m in
                   re.finditer(r'\{\s*(0x[0-9A-Fa-f]{8}),\s*([A-Za-z_0-9]+)\s*\}', init))

    below = [p for p in pairs if p[0] <= addr]
    above = [p for p in pairs if p[0] > addr]
    print('faixa registrada vizinha:')
    if below:
        print('  abaixo %08X %s (+%X bytes)' % (below[-1][0], below[-1][1], addr - below[-1][0]))
    if above:
        print('  acima  %08X %s (-%X bytes)' % (above[0][0], above[0][1], above[0][0] - addr))

    # branches (b/bl, com ou sem link) que apontam para o endereco
    base, n = BASE, len(img.data)
    brs = []
    for off in range(0, n - 3, 4):
        w = struct.unpack_from('>I', img.data, off)[0]
        if (w >> 26) == 18:
            li = w & 0x03FFFFFC
            if li & 0x02000000:
                li -= 0x04000000
            tgt = (base + off + li) & 0xFFFFFFFF if not (w & 2) else li
            if tgt == addr:
                brs.append((base + off, bool(w & 1)))
    print('branches para %08X: %d' % (addr, len(brs)))
    for a, link in brs[:10]:
        owner = [p for p in pairs if p[0] <= a]
        print('  %08X %s  (dentro de %s)' % (a, 'bl' if link else 'b',
                                             owner[-1][1] if owner else '?'))

    # ha algum branch de dentro da funcao abaixo para o endereco?
    if below:
        start = below[-1][0]
        region = []
        for off in range(start - BASE, min(addr, above[0][0] if above else addr) - BASE, 4):
            w = struct.unpack_from('>I', img.data, off)[0]
            if (w >> 26) == 18:
                li = w & 0x03FFFFFC
                if li & 0x02000000:
                    li -= 0x04000000
                tgt = (start + off + li) & 0xFFFFFFFF if not (w & 2) else li
                if tgt == addr:
                    region.append(start + off)
        print('branches de dentro de %s para o alvo: %s' % (below[-1][1],
                                                           [hex(x) for x in region]))


if __name__ == '__main__':
    main()