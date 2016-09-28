
# Copyright (C) 2006-2008 Junjiro Okajima
# Copyright (C) 2006-2008 Tomas Matejicek, slax.org
#
# LICENSE follows the described ones in lzma and squashfs.

# $Id: Makefile,v 1.30 2008-03-12 16:24:54 jro Exp $

# paths
Sqlzma = ${CURDIR}

LzmaVer =  
#Lzma = ${Sqlzma}/${LzmaVer}
Lzma = lzma457
SqVer = squashfs_4.0
Squashfs = ${SqVer}

TOPDIR := $(shell /bin/pwd)
SQUASHFS_VER="4.0"
SQUASHFS_DIR=$(TOPDIR)/squashfs_4.0
export Sqlzma=$(SQUASHFS_DIR)

export LzmaAlone=$(TOPDIR)/lzma457/CPP/7zip/Compress/LZMA_Alone
export LzmaC=$(TOPDIR)/lzma457/C/Compress/Lzma

SqTools = ${Squashfs}/squashfs-tools

# enable it if you want to add -g option when compiling
UseDebugFlags =
# disable it if you don't want to compile squashfs kernel module here
BuildSquashfs = 1

export

all:
	make -C $(LzmaAlone) -f sqlzma.mk
	make -C $(LzmaC) -f sqlzma.mk
	make -C $(SQUASHFS_DIR)

	#${MAKE} -C ${LzmaC} -f sqlzma.mk $@
	#${MAKE} -C ${LzmaAlone} -f sqlzma.mk $@
	#${MAKE} -C ${SqTools} $@

clean:
	${MAKE} -C ${LzmaC} -f sqlzma.mk $@
	${MAKE} -C ${LzmaAlone} -f sqlzma.mk $@
	${MAKE} -C ${SqTools} $@
	${RM} *~

########################################
