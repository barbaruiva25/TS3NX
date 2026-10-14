# NOTAS-DE-BUILD — TS3NX

- Host: Windows, Python 3.13 ok, Git ok. Pendente: clang 20 portátil, VS Build Tools libs, CMake, Ninja, devkitA64+libnx+switch-tools, `gh auth login`.
- Flags PC: `-march=x86-64-v2`, `tools/win/env.ps1` + `run.ps1`, `fetch_thirdparty.py` nos symlinks.
- Switch: sem `-march=native`; conferir `compile_commands.json` + `ninja -t graph` + desasm Cortex-A57.
- Testes PC sempre mutados + minimizados. Switch sempre em title takeover, com ZIP `switch/thesims3/thesims3.nro`.
