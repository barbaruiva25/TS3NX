"""Caracteriza um endereco guest do Sims3.xex: esta na tabela gerada? tem
chamadores diretos? o que o codigo faz? Deixa o diagnostico em stdout.

Uso: python ferramentas/addr_report.py 0x8907D040
"""
import glob
import io
import re
import struct
import sys

sys.path.insert(0, r'C:\Users\barba\Documents\xbox360\TS3NX\ferramentas')
from ppc_mini import Image, decode, text

IMG_PATH = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\LOGS\sims3_image.bin'
BASE = 0x88000000
GEN = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\generated\sims3'
OVR = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\overrides.toml'


def main():
    addr = int(sys.argv[1], 16)
    img = Image(IMG_PATH, BASE)

    # 1. esta na tabela de mapeamento gerada?
    init = io.open(GEN + r'\sims3_init.cpp', encoding='utf-8', errors='replace').read()
    mapped = re.search(r'\{\s*(0x%08X),\s*([A-Za-z_0-9]+)\s*\}' % addr, init)
    print('mapeado no gerado: %s' % (mapped.group(0) if mapped else 'NAO'))

    # 2. esta no overrides.toml?
    ovr = io.open(OVR, encoding='utf-8', errors='replace').read()
    in_ovr = ('"%08X"' % addr) in ovr
    print('no overrides.toml: %s' % in_ovr)

    # 3. vizinhos na tabela (a funcao mais proxima abaixo/acima)
    pairs = sorted((int(m.group(1), 16), m.group(2)) for m in
                   re.finditer(r'\{\s*(0x[0-9A-Fa-f]{8}),\s*([A-Za-z_0-9]+)\s*\}', init))
    below = [p for p in pairs if p[0] <= addr]
    if below:
        print('funcao registrada abaixo: %08X %s (delta +%X)' % (below[-1][0], below[-1][1],
                                                                 addr - below[-1][0]))

    # 4. quem chama direto (bl)?
    base, n = BASE, len(img.data)
    callers = []
    for off in range(0, n - 3, 4):
        w = struct.unpack_from('>I', img.data, off)[0]
        if (w >> 26) == 18 and (w & 1):
            li = w & 0x03FFFFFC
            if li & 0x02000000:
                li -= 0x04000000
            tgt = (base + off + li) & 0xFFFFFFFF if not (w & 2) else li
            if tgt == addr:
                callers.append(base + off)
    print('chamadores bl diretos: %d %s' % (len(callers), [hex(c) for c in callers[:8]]))

    # 5. disassembly no endereco
    print('--- codigo em %08X ---' % addr)
    a = addr
    for _ in range(28):
        ins = decode(img.word(a), a)
        print('  %08X %08X %s' % (a, ins.word, text(ins)))
        if ins.word == 0x4E800020:
            break
        a += 4


if __name__ == '__main__':
    main()