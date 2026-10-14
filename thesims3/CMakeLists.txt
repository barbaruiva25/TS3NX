# The Sims 3 (Xbox 360, title 454108E2): aplicacao PC de recompilacao estatica.
#
# O codigo do jogo nao esta neste repo: rode o codegen antes
# (rexglue codegen sims3_manifest.toml, daqui), que escreve generated/sims3
# a partir do seu Sims3.xex (generated/sims3/sources.cmake + generated/rexglue.cmake).
#
# Stage 1, Windows PC (dentro do env MSVC; clang 23 no PATH):
#   cmake -S thesims3 -B thesims3/out/pc -G Ninja -DCMAKE_BUILD_TYPE=Release
#   cmake --build thesims3/out/pc
# Requer: CMake 4+, Ninja, clang, VS Build Tools (link.exe).

cmake_minimum_required(VERSION 3.25)
project(sims3 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# O SDK e compilado do fonte salvo indicacao em contrario (reuso do fc3-nx, sem copiar).
set(REXSDK_DIR "C:/Users/barba/Documents/xbox360/FARCRY3/xbox360/fc3-nx/sdk" CACHE PATH "Arvore fonte do ReXGlue SDK")

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/generated/rexglue.cmake")
    message(FATAL_ERROR "generated/rexglue.cmake ausente: rode 'rexglue codegen sims3_manifest.toml' antes")
endif()
include(generated/rexglue.cmake)

# O SDK precisa de SSSE3 (memory.cpp usa _mm_shuffle_epi8).
add_compile_options(-march=x86-64-v2)

if(WIN32)
    add_executable(sims3 WIN32
        src/main.cpp
        src/thesims3_language.cpp
        src/thesims3_vfs.cpp
        src/thesims3_input.cpp
    )
else()
    add_executable(sims3
        src/main.cpp
        src/thesims3_language.cpp
        src/thesims3_vfs.cpp
        src/thesims3_input.cpp
    )
endif()

# Liga o SDK + o codigo gerado (GPU emulada Xenos no stage 1; renderer nativo na fase 4).
rexglue_setup_target(sims3 GPU_PLUGINS xenos)

target_include_directories(sims3 PRIVATE src)

# FMA fundido e aliasing agressivo mudam o resultado do PPC: o codigo gerado
# precisa de -ffp-contract=off -fno-strict-aliasing (clang do PC tambem).
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(sims3 PRIVATE -ffp-contract=off -fno-strict-aliasing)
endif()
