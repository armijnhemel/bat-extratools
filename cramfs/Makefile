all:	fsck.cramfs

OBJS = fsck.cramfs.o crc32.o blkdev.o linux_version.o cramfs_common.o

fsck.cramfs: fsck.cramfs.o crc32.o blkdev.o linux_version.o cramfs_common.o
	$(CC) $(OBJS) -lz -o $@
