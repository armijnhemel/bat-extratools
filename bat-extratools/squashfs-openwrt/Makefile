INCLUDEDIR = .

LZMAPATH = lzma-4.32/C/7zip/Compress/LZMA_Lib

CFLAGS := -I$(INCLUDEDIR) -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -O2

all: unsquashfs-lzma

unsquashfs-lzma: unsquashfs.o liblzma.a
	$(CXX) unsquashfs.o -L$(LZMAPATH) -llzma -o $@

liblzma.a:
	$(MAKE) -C $(LZMAPATH)

clean:
