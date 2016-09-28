/*
 * Copyright (c) 2010
 * Phillip Lougher <phillip@lougher.demon.co.uk>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2,
 * or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 * lzma_xz_wrapper.c
 *
 * Support for LZMA1 compression using XZ Utils liblzma http://tukaani.org/xz/
 */

#include <stdio.h>
#include <string.h>
#include "LzmaDecode.c"

#include "squashfs_fs.h"
#include "compressor.h"
#include "lzma_xz_options.h"

#define LZMA_PROPS_SIZE 5
#define LZMA_UNCOMP_SIZE 8
#define LZMA_HEADER_SIZE (LZMA_PROPS_SIZE + LZMA_UNCOMP_SIZE)

#define LZMA_OPTIONS 5
#define MEMLIMIT (32 * 1024 * 1024)

static int lzma_compress(void *dummy, void *dest, void *src,  int size,
	int block_size, int *error)
{
	return -1;
}


static int lzma_uncompress(void *dest, void *src, int size, int block_size,
	int *error)
{
	static unsigned char lzma_workspace[(LZMA_BASE_SIZE + (LZMA_LIT_SIZE << 3)) * sizeof(CProb)];
	int uncompressed_size = 0, res;
	unsigned char pb = 2, lp = 0, lc = 3;

	res = LzmaDecode(lzma_workspace, sizeof(lzma_workspace), lc, lp, pb, src, size, dest, block_size, &uncompressed_size);
	if (res == LZMA_RESULT_OK)
		return uncompressed_size;

	*error = res;
	return -1;
}

struct compressor gzip_comp_ops = {
	.init = NULL,
	.compress = lzma_compress,
	.uncompress = lzma_uncompress,
	.options = NULL,
	.usage = NULL,
	.id = ZLIB_COMPRESSION,
	.name = "gzip",
	.supported = 1
};

