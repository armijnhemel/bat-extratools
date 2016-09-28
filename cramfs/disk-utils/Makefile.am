include $(top_srcdir)/config/include-Makefile.am

utils_common = $(top_srcdir)/lib/blkdev.c
if LINUX
utils_common += $(top_srcdir)/lib/linux_version.c
endif

sbin_PROGRAMS = 

cramfs_common = $(utils_common) cramfs.h cramfs_common.c cramfs_common.h
sbin_PROGRAMS += fsck.cramfs
fsck_cramfs_SOURCES = fsck.cramfs.c $(cramfs_common)
fsck_cramfs_LDADD = -lz
