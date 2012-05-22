/* romfs_extract - check and optionally extract a ROMFS file system
 *
 * Copyright (C) 2004 Harald Welte <laforge@gnumonks.org>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * Version 2 as published by the Free Software Foundation.
 *
 */

/*
 * Warning!  Not fully implemented yet, and spaghetti code. Patches welcome.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <fnmatch.h>
#include <dirent.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/mman.h>

#include <netinet/in.h>

struct romfh {
	int32_t nextfh;
	int32_t spec;
	int32_t size;
	int32_t checksum;
};

#define ROMFS_MAXFN 128
#define ROMFH_HRD 0
#define ROMFH_DIR 1
#define ROMFH_REG 2
#define ROMFH_LNK 3
#define ROMFH_BLK 4
#define ROMFH_CHR 5
#define ROMFH_SCK 6
#define ROMFH_FIF 7
#define ROMFH_EXEC 8

struct node_info {
	u_int32_t nextfh;
	u_int32_t spec;
	u_int32_t size;
	u_int32_t checksum;
	char *name;
	void *file;
	u_int32_t mode;
	unsigned int namelen;
};

static int parse_node(void *start, unsigned int offset, struct node_info *ni)
{
	struct romfh *rfh = start + offset;
	void *nameend;

	ni->size = ntohl(rfh->size);
	ni->mode = (ntohl(rfh->nextfh) & 0x0f);
	ni->nextfh = ntohl(rfh->nextfh) & ~0x0f;
	ni->checksum = ntohl(rfh->checksum);
	ni->spec = ntohl(rfh->spec);
	ni->name = (char *) (rfh+1);

	ni->namelen = strlen(ni->name);
	nameend = (void *) ((unsigned long)ni->name + ni->namelen) 
			    - (unsigned long )start;
	if ((unsigned long)nameend&15) {
		nameend = ((unsigned long) nameend&~15)+16;
		ni->namelen = nameend - ((void *)ni->name - start);
	}

	ni->file = (char *)ni->name + ni->namelen;
}

static int recurse(void *mem, unsigned int offset, const char *dir)
{
	int ret, outfd;
	unsigned int mode;
	struct node_info ni;

	while (1) {
		printf("==========================\n");
		printf("parse_node(%u/0x%x)\n", offset, offset);
		parse_node(mem, offset, &ni);
		printf("%s: ", ni.name);

		switch (ni.mode & ~ROMFH_EXEC) {
		case ROMFH_HRD:
			printf("hard link\n");
			if (ni.size)
				fprintf(stderr, "nonstandard size `%u'\n",
					ni.size);
			break;
		case ROMFH_DIR:
			printf("directory\n");
			if (ni.size)
				fprintf(stderr, "nonstandard size `%u'\n",
					ni.size);
			if (!strcmp(ni.name, "..")
			    || !strcmp(ni.name, ".")) {
				fprintf(stderr, "name invalid!!\n");
				break;
			}
			if (mkdir(ni.name, 0750) < 0) {
				fprintf(stderr, "can't create `%s': %s\n",
					ni.name, strerror(errno));
				return -1;
			}
			chdir(ni.name);

			if (ni.spec != offset) {
				ret = recurse(mem, ni.spec, dir);
				chdir("..");
				if (ret < 0)
					return ret;
			}
			break;
		case ROMFH_REG:
			printf("regular file\n");
			mode = 0640;
			if (ni.mode & ROMFH_EXEC)
				mode |= 0110;

			outfd = creat(ni.name, mode);
			if (outfd < 0) {
				fprintf(stderr, "can't create `%s': %s\n",
					ni.name, strerror(errno));
				return -1;
			}
			if (write(outfd, ni.file, ni.size) < ni.size) {
				fprintf(stderr, "short write `%s': %s\n",
					ni.name, strerror(errno));
				close(outfd);
				return -1;
			}
			close(outfd);
			break;
		case ROMFH_LNK:
			printf("symbolic link\n");
			break;
		case ROMFH_BLK:
			printf("block device\n");
			if (ni.size)
				fprintf(stderr, "nonstandard size `%u'\n",
					ni.size);
			break;
		case ROMFH_CHR:
			printf("character device\n");
			if (ni.size)
				fprintf(stderr, "nonstandard size `%u'\n",
					ni.size);
			break;
		case ROMFH_SCK:
			printf("socket\n");
			if (ni.size)
				fprintf(stderr, "nonstandard size `%u'\n",
					ni.size);
			break;
		case ROMFH_FIF:
			printf("fifo\n");
			if (ni.size)
				fprintf(stderr, "nonstandard size `%u'\n",
					ni.size);
			break;
		}

		if (!ni.nextfh)
			return 1;

		printf("nextfh=%u\n", ni.nextfh);

		offset = ni.nextfh;
		//curmem += ni.nextfh;
	}
	/* not reached */
	return -10;
}


static int extract_from_mem(void *mem, unsigned int len, const char *dir)
{
	unsigned int offset = 0;
	struct node_info ni;

	//ri.checksum = htonl(0x55555555);
	//
	parse_node(mem, offset, &ni);
	printf("+= %u + %u\n", sizeof(struct romfh), ni.namelen);
	offset += sizeof(struct romfh) + ni.namelen;

	printf("romfs image name: `%s'\n", ni.name);
	printf("romfs image size: %u\n", ni.size);

	return recurse(mem, offset, dir);
}


static int extract(const char *pathname, const char *outpath)
{
	int fd, ret = -1;
	struct stat st;
	void *mem;

	fd = open(pathname, O_RDONLY);
	if (fd < 0) {
		fprintf(stderr, "Error opening `%s': %s\n", pathname,
			strerror(errno));
		goto err_out;
	}

	if (fstat(fd, &st) < 0) {
		fprintf(stderr, "Error in fstat: %s\n", strerror(errno));
		goto err_close;
	}

	mem = mmap(NULL, st.st_size, PROT_READ, MAP_SHARED, fd, 0);
	if (!mem) {
		fprintf(stderr, "Error during MMAP: %s\n", strerror(errno));
		goto err_close;
	}

	if (strncmp((char *)mem, "-rom1fs-", 8)) {
		fprintf(stderr,"File is not a romfs image\n");
		goto err_unmap;
	}

	ret = extract_from_mem(mem, st.st_size, outpath);

err_unmap:
	munmap(mem, st.st_size);
err_close:
	close(fd);
err_out:
	return ret;
}

static char *cmdname;

static void version(void)
{
	fprintf(stderr, "%s, Version 0.01\n", cmdname);
	fprintf(stderr, "(C) 2004 by Harald Welte <laforge@gnumonks.org\n");
	fprintf(stderr, "This program is Free Software covered by GNU GPLv2\n");
}

static void usage(void)
{
	version();
	fprintf(stderr, "Not implemented yet\n");
}

int main(int argc, char **argv)
{
	int c;
	char *outdir = NULL;
	char basedir[PATH_MAX+1];

	cmdname = argv[0];

	while ((c = getopt(argc, argv, "V:x:h")) != EOF) {
		switch (c) {
		case 'x':
			outdir = optarg;
			break;
		case 'h':
			usage();
			exit(0);
			break;
		case 'V':
			version();
			exit(0);
			break;
		}
	}

	if (argc <= optind) {
		usage();
		exit(2);
	}

	if (outdir) {
		if (chdir(outdir) < 0) {
			if (mkdir(outdir, 0750) < 0) {
				fprintf(stderr, "unable to create `%s': %s\n",
					strerror(errno));
				exit(1);
			}
			chdir(outdir);
		}
	}

	if (extract(argv[optind], outdir) < 0)
		exit(1);

	exit(0);
}
