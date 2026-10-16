"""Emula o default.xex do entry com contexto zerado (semantica Xenia) e stubs
de kernel, ate a chamada no Sims3.xex. Responde EXATAMENTE quais registradores
o jogo recebe. Para na primeira bctrl para 0x88xxxxxx e relata tudo.

Stubs (Xenia, sem launch data): XexLoadImage -> handle; GetProcAddress ->
enderecos reais (ord 3 -> 0x88329E10, ord 1 -> 0x88329E58); GetLaunchData* ->
NOT_FOUND; resto -> 0 (r3), demais regs preservados.
Memoria: imagem + stack/heap dict. Syscalls so escrevem r3.
Uso: python ferramentas/chain_emu.py
"""
import struct
import sys

sys.path.insert(0, r'C:\Users\barba\Documents\xbox360\TS3NX\ferramentas')
from ppc_mini import Image, decode

IMG = Image(r'C:\Users\barba\Documents\xbox360\TS3NX\thesims3\LOGS\default_image.bin', 0x82000000)

ORD3 = 0x88329E10
ORD1 = 0x88329E58
HANDLE = 0xF8000028
NOT_FOUND = 0xC0000225

mem_extra = {}


def ld32(a):
    if IMG.contains(a, 4):
        return struct.unpack_from('>I', IMG.data, a - IMG.base)[0]
    return mem_extra.get(a & 0xFFFFFFFF, 0)


def st32(a, v):
    a &= 0xFFFFFFFF
    if IMG.contains(a, 4):
        return
    mem_extra[a] = v & 0xFFFFFFFF


regs = [0] * 32
regs[1] = 0x70160000
regs[13] = 0x70000000
ctr = 0
cr = [0] * 8
lr = 0
carry_ca = 0
CALL_LOG = []


def rlwinm(v, sh, mb, me):
    r = ((v << sh) | (v >> (32 - sh))) & 0xFFFFFFFF if sh else v & 0xFFFFFFFF
    m = 0
    for i in range(32):
        on = (mb <= i <= me) if mb <= me else (i >= mb or i <= me)
        if on:
            m |= 1 << (31 - i)
    return r & m


def is_thunk(tgt):
    try:
        w = (IMG.word(tgt), IMG.word(tgt + 4), IMG.word(tgt + 8), IMG.word(tgt + 12))
    except Exception:
        return False
    return (w[0] >> 24) == 0x01 and (w[1] >> 24) == 0x02 and w[2] == 0x7D6903A6 and w[3] == 0x4E800420


def do_kernel(tgt):
    if tgt == 0x820A6F10:  # XexLoadImage(path=r3,?,\u2009?,out=r6?): r3=handle
        # wrapper default le handle de [r1+80]; escreve la:
        CALL_LOG.append('XexLoadImage -> handle')
        return HANDLE
    if tgt == 0x820A6F00:  # XexGetProcedureAddress(h=r3, ord=r4, out=r5)
        h, o, out = regs[3], regs[4], regs[5]
        addr = {3: ORD3, 1: ORD1, 2: 0x885A5670}.get(o, 0)
        st32(out, addr)
        CALL_LOG.append('GetProcAddress(h=%08X, ord=%d) -> %08X' % (h, o, addr))
        return 0
    if tgt == 0x820A6E20:  # GetLaunchDataSize
        st32(regs[3], 0)
        CALL_LOG.append('GetLaunchDataSize -> NOT_FOUND')
        return NOT_FOUND
    if tgt == 0x820A6E10:
        CALL_LOG.append('GetLaunchData -> NOT_FOUND')
        return NOT_FOUND
    if tgt == 0x820A6E30:
        CALL_LOG.append('SetLaunchData ok')
        return 0
    if tgt == 0x820A6EB0:
        CALL_LOG.append('XGetLanguage -> 13')
        return 13
    CALL_LOG.append('kernel %08X -> 0' % tgt)
    return 0


def run(entry):
    global ctr, lr, carry_ca
    pc = entry
    stack = []
    steps = 0
    trail = []
    while steps < 2000000:
        steps += 1
        trail.append(pc)
        if len(trail) > 40:
            trail.pop(0)
        if not IMG.contains(pc, 4):
            print('pc fora da imagem em %08X (passos %d)' % (pc, steps))
            print('rastreio:', ' '.join('%08X' % a for a in trail))
            print('r3=%08X r4=%08X r5=%08X r6=%08X r7=%08X r8=%08X ctr=%08X lr=%08X' %
                  (regs[3], regs[4], regs[5], regs[6], regs[7], regs[8], ctr, lr))
            for c in CALL_LOG[-12:]:
                print('  ', c)
            return
        ins = decode(IMG.word(pc), pc)
        op, w = ins.op, ins.word
        rt, ra, rb = ins.rt, ins.ra, ins.rb
        imm = ins.imm if ins.imm is not None else 0
        s16 = imm - 0x10000 if imm & 0x8000 else imm
        if op == 'lis':
            regs[rt] = (imm << 16) & 0xFFFFFFFF
        elif op == 'li':
            regs[rt] = s16 & 0xFFFFFFFF
        elif op == 'addi':
            regs[rt] = ((0 if ra == 0 else regs[ra]) + s16) & 0xFFFFFFFF
        elif op == 'addis':
            regs[rt] = ((0 if ra == 0 else regs[ra]) + (imm << 16)) & 0xFFFFFFFF
        elif op == 'add':
            regs[rt] = (regs[ra] + regs[rb]) & 0xFFFFFFFF
        elif op == 'subf':
            regs[rt] = (regs[rb] - regs[ra]) & 0xFFFFFFFF
        elif op == 'arith':
            # familia com carry. CA global.
            global carry_ca
            xo9 = (w >> 1) & 0x1FF
            a, b = regs[ra], regs[rb]
            M = 0xFFFFFFFF
            if xo9 == 10:  # addc
                full = a + b
            elif xo9 == 138:  # adde
                full = a + b + carry_ca
            elif xo9 == 234:  # addme
                full = a + carry_ca - 1
            elif xo9 == 202:  # addze
                full = a + carry_ca
            elif xo9 == 8:  # subfc
                full = b + (~a & M) + 1
            elif xo9 == 136:  # subfe
                full = b + (~a & M) + carry_ca
            elif xo9 == 232:  # subfme
                full = (~a & M) + carry_ca - 1 + 0x100000000
            elif xo9 == 200:  # subfze
                full = (~a & M) + carry_ca
            else:
                print('XO arith?', xo9, hex(pc))
                return
            carry_ca = 1 if full >= 0x100000000 else 0
            regs[rt] = full & M
            if w & 1:
                cr[0] = 0b0010 if regs[rt] == 0 else (0b1000 if False else 0)
        elif op in ('addic', 'subfic', 'addic.'):
            a = regs[ra]
            if op == 'subfic':
                full = s16 + (~a & 0xFFFFFFFF) + 1
            else:
                full = a + s16
            carry_ca = 1 if full >= 0x100000000 else 0
            regs[rt] = full & 0xFFFFFFFF
            if op == 'addic.':
                cr[0] = 0b0010 if regs[rt] == 0 else 0
        elif op == 'mulli':
            regs[rt] = (regs[ra] * s16) & 0xFFFFFFFF
        elif op == 'mr':
            regs[ra] = regs[rt]
        elif op == 'srawi':
            sh = rb
            v = regs[rt]
            regs[ra] = ((v if v < 0x80000000 else v - 0x100000000) >> sh) & 0xFFFFFFFF
        elif op in ('slw', 'srw', 'sraw'):
            sh = regs[rb] & 0x3F
            v = regs[rt]
            if op == 'slw':
                regs[ra] = (v << sh) & 0xFFFFFFFF if sh < 32 else 0
            elif op == 'srw':
                regs[ra] = (v >> sh) if sh < 32 else 0
            else:
                regs[ra] = ((v if v < 0x80000000 else v - 0x100000000) >> sh) & 0xFFFFFFFF if sh < 32 else (0xFFFFFFFF if v >= 0x80000000 else 0)
        elif op in ('and', 'or', 'xor', 'logic'):
            a, b = regs[rt], regs[rb]
            if op == 'and' or (op == 'logic' and False):
                regs[ra] = a & b
            elif op == 'or':
                regs[ra] = a | b
            elif op == 'xor':
                regs[ra] = a ^ b
            else:
                print('logic?', op, hex(pc), hex(w))
                return
        elif op in ('ori', 'oris', 'xori'):
            regs[ra] = (regs[rt] | (imm if op == 'ori' else (imm << 16))) & 0xFFFFFFFF
        elif op in ('rlwinm', 'rlwimi'):
            v = rlwinm(regs[rt], ins.sh, ins.mb, ins.me)
            if op == 'rlwimi':
                m = 0
                for i in range(32):
                    on = (ins.mb <= i <= ins.me) if ins.mb <= ins.me else (i >= ins.mb or i <= ins.me)
                    if on:
                        m |= 1 << (31 - i)
                v = (v & m) | (regs[ra] & ~m & 0xFFFFFFFF)
            regs[ra] = v & 0xFFFFFFFF
            if ins.rc:
                cr[0] = 0b0010 if regs[ra] == 0 else 0
        elif op == 'andi.':
            regs[ra] = regs[rt] & imm
            cr[0] = 0b0010 if regs[ra] == 0 else 0
        elif op in ('cmpli', 'cmpi'):
            a = regs[ra]
            b = imm if op == 'cmpli' else s16
            f = rt >> 2
            cr[f] = (0b1000 if a < b else 0) | (0b0010 if a == b else 0) | (0b0001 if a > b else 0)
        elif op in ('cmp', 'cmpl'):
            a, b = regs[ra], regs[rb]
            f = rt >> 2
            cr[f] = (0b1000 if a < b else 0) | (0b0010 if a == b else 0) | (0b0001 if a > b else 0)
        elif op in ('lwz', 'stw', 'lbz', 'stb', 'lhz', 'sth'):
            ea = ((0 if ra == 0 else regs[ra]) + s16) & 0xFFFFFFFF
            if op == 'lwz':
                regs[rt] = ld32(ea)
            elif op == 'stw':
                st32(ea, regs[rt])
            elif op == 'lbz':
                regs[rt] = ld32(ea & ~3) >> (8 * (3 - (ea & 3))) & 0xFF
            elif op == 'stb':
                a4 = ea & ~3
                cur = ld32(a4)
                sh = 8 * (3 - (ea & 3))
                st32(a4, (cur & ~(0xFF << sh)) | ((regs[rt] & 0xFF) << sh))
            elif op == 'lhz':
                regs[rt] = ld32(ea & ~3) >> (8 * (2 - (ea & 2))) & 0xFFFF
            elif op == 'sth':
                a4 = ea & ~3
                cur = ld32(a4)
                sh = 8 * (2 - (ea & 2))
                st32(a4, (cur & ~(0xFFFF << sh)) | ((regs[rt] & 0xFFFF) << sh))
        elif op in ('ld', 'st', 'stu'):
            ds = (w & 0xFFFC) - (0x10000 if w & 0x8000 else 0)
            ea = (regs[ra] + ds) & 0xFFFFFFFF
            if op == 'ld':
                q = w & 3
                regs[rt] = (ld32(ea) << 32) | ld32(ea + 4)
                if q == 1:
                    regs[ra] = ea
            else:
                st32(ea, (regs[rt] >> 32) & 0xFFFFFFFF)
                st32(ea + 4, regs[rt] & 0xFFFFFFFF)
                if op == 'stu':
                    regs[ra] = ea
        elif op == 'lmw':
            a0 = (regs[ra] + s16) & 0xFFFFFFFF
            for i in range(rt, 32):
                regs[i] = ld32(a0)
                a0 += 4
        elif op == 'mfspr':
            spr = ((w >> 16) & 31) | (((w >> 11) & 31) << 5)
            if spr == 8:
                regs[rt] = lr
            elif spr == 9:
                regs[rt] = ctr
            else:
                print('mfspr spr?', spr, hex(pc))
                return
        elif op == 'mtlr':
            lr = regs[rt]
        elif op == 'mtctr':
            ctr = regs[rt]
        elif op in ('mtcrf', 'mcrf', 'mfcr', 'crop'):
            if op == 'mfcr':
                regs[rt] = 0
        elif op == 'b':
            if ins.link:
                lr = pc + 4
                if 0x88000000 <= ins.target < 0x89500000:
                    print('CHAMADA SIMS3 (bl) em %08X -> %08X' % (pc, ins.target))
                    print('r3=%08X r4=%08X r5=%08X r6=%08X r7=%08X' % tuple(regs[i] for i in (3, 4, 5, 6, 7)))
                    print('r25-r31:', ' '.join('%08X' % regs[i] for i in range(25, 32)))
                    print('r8=%08X' % regs[8])
                    return
                if is_thunk(ins.target):
                    regs[3] = do_kernel(ins.target)
                    pc += 4
                    continue
                stack.append(pc + 4)
                pc = ins.target
                continue
            else:
                pc = ins.target
                continue
        elif op in ('bclr', 'bcctr'):
            bo, bi = ins.bo, ins.bi
            if bo & 0x10:
                cond_ok = True
            else:
                cbit = (cr[bi >> 2] >> (3 - (bi & 3))) & 1
                cond_ok = bool(cbit) == bool(bo & 0x08)
            if not cond_ok:
                pc += 4
                continue
            if ins.link:
                lr = pc + 4
            if op == 'bcctr':
                tgt = ctr
                if 0x88000000 <= tgt < 0x89500000:
                    print('CHAMADA SIMS3 em %08X -> %08X' % (pc, tgt))
                    print('r3=%08X r4=%08X r5=%08X r6=%08X r7=%08X' % tuple(regs[i] for i in (3, 4, 5, 6, 7)))
                    print('r25-r31:', ' '.join('%08X' % regs[i] for i in range(25, 32)))
                    print('r8=%08X' % regs[8])
                    return
                pc = tgt
                continue
            else:
                if not stack:
                    print('retorno fora da pilha em', hex(pc))
                    return
                pc = stack.pop()
                continue
        elif op == 'bc':
            bo, bi = ins.bo, ins.bi
            ctr_ok = True
            if not (bo & 0x04):
                ctr = (ctr - 1) & 0xFFFFFFFFFFFFFFFF
                ctr_ok = (ctr != 0) ^ bool(bo & 0x02)
            if bo & 0x10:
                cond_ok = True
            else:
                cbit = (cr[bi >> 2] >> (3 - (bi & 3))) & 1
                cond_ok = bool(cbit) == bool(bo & 0x08)
            pc = ins.target if (ctr_ok and cond_ok) else pc + 4
            continue
        elif op in ('tw', 'twi'):
            pass
        elif op == 'x31':
            print('x31 nao tratada em', hex(pc), hex(w))
            return
        else:
            print('op?', op, hex(pc))
            return
        pc += 4
    print('steps esgotados')
    print('r3=%08X r4=%08X r5=%08X r6=%08X r7=%08X' % tuple(regs[i] for i in (3, 4, 5, 6, 7)))
    for c in CALL_LOG[-20:]:
        print('  ', c)


if __name__ == '__main__':
    run(0x82041028)
