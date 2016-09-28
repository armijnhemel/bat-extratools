INCLUDEDIR = .
LZMAPATH = ./lzma/C/7zip/Compress/LZMA_Lib

CFLAGS := -I$(INCLUDEDIR) -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -O2 

all: bat-unsquashfs-atheros2
CC=gcc
CXX=g++

bat-unsquashfs-atheros2: unsquashfs.o liblzma.a
	$(CXX) unsquashfs.o -L$(LZMAPATH) -llzma -o $@

liblzma.a:
	$(MAKE) -C $(LZMAPATH)
