"""Acha o par de instrucoes que materializa um endereco guest em codigo
(lis + addi/addis/ori, nas duas formas de 32 bits). Serve de evidencia para
uma entrada do overrides.toml: o alvo so e alcancado por ponteiro construido
em runtime.

Uso: python ferramentas/find_addr_build.py 0x8907D040
"""
import struct
import sys

IMG_PATH = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\LOGS\sims3_image.bin'
BASE = 0x88000000


def lis_sites(d, hi):
    """(offset, reg) de todo lis rX, hi."""
    out = []
    for off in range(0, len(d) - 3, 4):
        w = struct.unpack_from('>I', d, off)[0]
        if (w >> 26) == 15 and ((w >> 16) & 31) == 0 and ((w >> 21) & 31) != 0 and (w & 0xFFFF) == hi:
            out.append((off, (w >> 21) & 31))
    return out


def main():
    addr = int(sys.argv[1], 16)
    d = open(IMG_PATH, 'rb').read()
    hi, lo = (addr >> 16) & 0xFFFF, addr & 0xFFFF
    formas = [(hi, lo, 'lis+ori'),
              (hi, lo - 0x10000 if lo >= 0x8000 else lo, 'lis+addi'),
              ((hi + 1) & 0xFFFF, (lo - 0x10000) & 0xFFFF, 'lis+addi(-16bits)')]
    total = 0
    for h, l, nome in formas:
        for off, reg in lis_sites(d, h):
            for k in range(1, 9):
                y = struct.unpack_from('>I', d, off + 4 * k)[0]
                op = y >> 26
                ra = (y >> 16) & 31
                imm = y & 0xFFFF
                simm = imm - 0x10000 if imm & 0x8000 else imm
                if op in (14, 15) and ra == reg and (imm & 0xFFFF) == (l & 0xFFFF):
                    a = BASE + off + 4 * k
                    print('%s: lis em %08X (r%d) + instrucao em %08X' % (nome, BASE + off, reg, a))
                    for j in range(max(0, off - 8), min(len(d), off + 4 * (k + 2)), 4):
                        pass
                    total += 1
                    break
    print('pares encontrados:', total)


if __name__ == '__main__':
    main()