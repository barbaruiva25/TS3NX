#!/usr/bin/env python3
"""Pos-codegen do TS3NX: roda apos TODO codegen (o gerador reescreve a arvore
e apaga os reparos). Ordem fixa, igual ao fc3-nx:

  1. fix_cross_file_labels.py      envolve blocos com goto cross-file
  2. fix_cross_file_branch_sites.py   reescreve os gotos para o wrapper
  3. lift_label_wrappers.py           sobe wrappers para escopo de arquivo
  4. fix_cross_file_branch_calls.py   goto wrapper(...) -> { wrapper(); return; }
  5. expand_wrapper_88D79634.py       o bloco 88D79634 desvia para o epilogo da
     propria funcao: o wrapper leva a copia exata do corpo de sub_88D794B0
     (frame -112 ja montado pelo chamador 88D79100; epilogo equilibra).

  python ferramentas/post_codegen.py [--check]
"""
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(TOOLS, '..', 'thesims3', 'generated', 'sims3')


def run(*args):
    r = subprocess.run([sys.executable, *args], cwd=TOOLS)
    if r.returncode != 0:
        sys.exit('post_codegen falhou em %s (%d)' % (args[0], r.returncode))


def main():
    check = ['--check'] if '--check' in sys.argv[1:] else []
    run(os.path.join(TOOLS, 'fix_cross_file_labels.py'), '--gen', GEN, *check)
    run(os.path.join(TOOLS, 'fix_cross_file_branch_sites.py'), '--gen', GEN, *check)
    run(os.path.join(TOOLS, 'lift_label_wrappers.py'), '--gen', GEN, *check)
    run(os.path.join(TOOLS, 'fix_cross_file_branch_calls.py'), '--gen', GEN, *check)
    if not check:
        run(os.path.join(TOOLS, 'expand_wrapper_88D79634.py'))


if __name__ == '__main__':
    main()
