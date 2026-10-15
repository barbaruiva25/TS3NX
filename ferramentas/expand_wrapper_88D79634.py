"""Expande o wrapper sims3_label_88D79634: bloco original (extraido pelo
fix_cross_file_labels) + copia do restante de sub_88D794B0, labels renomeados.

Motivo: o bloco 88D79634 desvia para 88D79660/88D7956C (epilogo da propria
funcao). Wrapper so com o bloco deixa gotos pendurados. A expansao e exata:
mesmas instrucoes, mesma ordem; frame (-112) montado pelo chamador
88D79100 (mesmo prologo), epilogo (+112 + return) equilibra, igual ao HW.
O prologo da copia (mflr/bl save/stwu) e descartado: no HW ele nao executa
nessa entrada. ABORTA se goto pendurado.
"""
import io
import re
import sys

P = r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\generated\sims3\sims3_recomp.92.cpp'
TAG = 'sims3_label_88D79634'
FUNC = 'sub_88D794B0'
PFX = 'w88D79634_'

lines = io.open(P, encoding='utf-8').read().split('\n')
ren = re.compile(r'\bloc_([0-9A-Fa-f]+)')


def take_braced(start):
    depth = 0
    for j in range(start, len(lines)):
        depth += lines[j].count('{') - lines[j].count('}')
        if j > start and depth == 0 and lines[j].rstrip() == '}':
            return start, j
    raise AssertionError('sem fim')


# 1. Corpo do wrapper antigo (bloco original extraido).
wstart = next(i for i, ln in enumerate(lines)
              if ln.startswith('extern "C" void ' + TAG + '('))
_, wend = take_braced(wstart)
old_body = lines[wstart + 1:wend]

# 2. Resto de sub_88D794B0 sem o prologo (a partir do primeiro label).
fdef = next(i for i, ln in enumerate(lines) if ln.startswith('DEFINE_REX_FUNC(' + FUNC + ')'))
_, fend = take_braced(fdef)
rest = lines[fdef + 1:fend]
first_label = next(i for i, ln in enumerate(rest) if re.match(r'^(loc_[0-9A-Fa-f]+):', ln.strip()))
rest = rest[first_label:]

new_body = ([ren.sub(lambda m: PFX + 'loc_' + m.group(1), ln) for ln in old_body]
            + [ren.sub(lambda m: PFX + 'loc_' + m.group(1), ln) for ln in rest])

wrapper = ['extern "C" void ' + TAG + '(PPCContext& __restrict ctx, uint8_t* base) {',
           '\tPPCRegister temp{};',
           '\tuint32_t ea{};']
wrapper += new_body
wrapper += ['}']

# 3. Troca o wrapper antigo pelo expandido.
del lines[wstart:wend + 1]
last_inc = max(i for i, ln in enumerate(lines) if ln.startswith('#include'))
lines[last_inc + 1:last_inc + 1] = [''] + wrapper + ['']

# 4. Confere: todo goto tem label.
text = '\n'.join(lines)
defs = set(m.group(1) for m in re.finditer(r'^((?:' + PFX + r')?loc_[0-9A-Fa-f]+):', text, re.M))
uses = set(m.group(1) for m in re.finditer(r'goto\s+((?:' + PFX + r')?loc_[0-9A-Fa-f]+)\s*[;(]', text))
dangling = sorted(u for u in uses if u not in defs)
if dangling:
    print('PENDURADOS:', dangling[:20])
    sys.exit(1)

io.open(P, 'w', encoding='utf-8', newline='').write(text)
print('wrapper expandido ok; labels defs:', len(defs))
