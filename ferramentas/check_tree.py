"""Confere a arvore gerada inteira: todo goto tem destino (label no mesmo
arquivo ou wrapper com definicao). So reporta; exit 1 se pendurado."""
import glob
import re
import sys

GEN = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\generated\sims3'

wrappers = set()
files = {}
for p in glob.glob(GEN + '/sims3_recomp.*.cpp'):
    t = open(p, errors='replace').read()
    files[p] = t
    for m in re.finditer(r'void\s+(sims3_label_[0-9A-Fa-f]+)\s*\(PPCContext&', t):
        wrappers.add(m.group(1).upper())

bad = []
for p, t in files.items():
    defs = set(m.group(1).upper() for m in re.finditer(r'^(?:w88D79634_)?(loc_[0-9A-Fa-f]+):', t, re.M))
    for m in re.finditer(r'goto\s+(sims3_label_[0-9A-Fa-f]+)\s*\(', t):
        if m.group(1).upper() not in wrappers:
            bad.append((p.split('\\')[-1], m.group(1), 'wrapper sem definicao'))
    for m in re.finditer(r'goto\s+(loc_[0-9A-Fa-f]+)\s*;', t):
        if m.group(1).upper() not in defs:
            bad.append((p.split('\\')[-1], m.group(1), 'label fora do arquivo'))
for b in bad:
    print(b)
print('total:', len(bad))
sys.exit(1 if bad else 0)
