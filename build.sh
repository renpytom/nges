#!/bin/bash

set -xe

RENPY_BUILD=${RENPY_BUILD:-/home/tom/ab/renpy-build}

build_all() {

    . $RENPY_BUILD/tmp/install.$1/env.sh

    dest=build/$1

    build () {
        obj=$1.o
        src=$1.cc
        mkdir -p $(dirname $dest/$obj)
        $CXX $CXXFLAGS -Isrc/ANESE/src -c $src -o $dest/$obj
    }

    mkdir -p $dest

    build src/ANESE/src/common/serializable
    build src/ANESE/src/nes/wiring/interrupt_lines
    build src/ANESE/src/nes/wiring/ppu_mmu
    build src/ANESE/src/nes/wiring/cpu_mmu
    build src/ANESE/src/nes/joy/joy
    build src/ANESE/src/nes/joy/controllers/standard
    build src/ANESE/src/nes/joy/controllers/zapper
    build src/ANESE/src/nes/nes
    build src/ANESE/src/nes/ppu/ppu
    build src/ANESE/src/nes/cpu/nestest
    build src/ANESE/src/nes/cpu/cpu
    build src/ANESE/src/nes/generic/ram/ram
    build src/ANESE/src/nes/generic/rom/rom
    build src/ANESE/src/nes/apu/apu
    build src/ANESE/src/nes/cartridge/mapper
    build src/ANESE/src/nes/cartridge/parse_rom
    build src/ANESE/src/nes/cartridge/mappers/mapper_003
    build src/ANESE/src/nes/cartridge/mappers/mapper_001
    build src/ANESE/src/nes/cartridge/mappers/mapper_007
    build src/ANESE/src/nes/cartridge/mappers/mapper_002
    build src/ANESE/src/nes/cartridge/mappers/mapper_009
    build src/ANESE/src/nes/cartridge/mappers/mapper_004
    build src/ANESE/src/nes/cartridge/mappers/mapper_000
    build src/api

    $CXX $CXXFLAGS $LDFLAGS -shared -o $dest/libnges-$1.$2 $(find $dest -name "*.o")
    $STRIP $dest/libnges-$1.$2
}

build_all linux-x86_64 so
build_all windows-x86_64 dll
build_all mac-x86_64 dylib
build_all mac-arm64 dylib
