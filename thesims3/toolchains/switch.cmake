# Toolchain Switch — devkitA64 + libnx (stub validado na etapa 5)
# Uso:
# cmake -S . -B out/build-normal -G Ninja -DCMAKE_TOOLCHAIN_FILE=thesims3/toolchains/switch.cmake -DCMAKE_BUILD_TYPE=Release
# Depois conferir compile_commands.json, ninja -t graph thesims3.nro, desasm Cortex-A57. Sem -march=native.
cmake_minimum_required(VERSION 3.28)
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
# Ajuste estes caminhos para o seu devkitPro instalado:
# set(DEVKITPRO $ENV{DEVKITPRO})
# set(DEVKITA64 ${DEVKITPRO}/devkitA64)
# set(CMAKE_C_COMPILER ${DEVKITA64}/bin/aarch64-none-elf-gcc)
# set(CMAKE_CXX_COMPILER ${DEVKITA64}/bin/aarch64-none-elf-g++)
# add_compile_options(-mcpu=cortex-a57 -O2)
# add_link_options(-specs=${DEVKITPRO}/libnx/switch.specs)
