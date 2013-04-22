#!/usr/bin/python

import sys, os, os.path, struct

'''
Yaffs2 unpacker reimplemention, heavily borrowing from unyaffs created
by Kai Wei

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.

'''

## some hardcoded settings copied from unyaffs.c and unyaffs.h
## In other devices these settings are actually different
CHUNK_SIZE=2048
SPARE_SIZE=64
MAX_OBJECTS=10000
YAFFS_OBJECTID_ROOT=1
YAFFS_MAX_NAME_LENGTH=255
YAFFS_MAX_ALIAS_LENGTH=159

YAFFS_OBJECT_TYPE_UNKNOWN = 0
YAFFS_OBJECT_TYPE_FILE = 1
YAFFS_OBJECT_TYPE_SYMLINK = 2
YAFFS_OBJECT_TYPE_DIRECTORY = 3
YAFFS_OBJECT_TYPE_HARDLINK = 4
YAFFS_OBJECT_TYPE_SPECIAL = 5

## test file system from one of those Realtek based devices
image_file = open('yaffs2_1.img')

image_file.seek(0)
bytesread = 0

yaffs2filesize = os.stat('yaffs2_1.img').st_size

if yaffs2filesize%(CHUNK_SIZE + SPARE_SIZE) != 0:
	## this is not a valid yaffs2 file for this chunk size and spare size
	sys.exit(1)

objectidtoname = {}
objectparent = {}

## read in the blocks of data
while not bytesread >= os.stat('yaffs2_1.img').st_size:
	chunkdata = image_file.read(CHUNK_SIZE)
	sparedata = image_file.read(SPARE_SIZE)

	## read in the spare data first and extract some metadata
	sequenceNumber = struct.unpack('<L', sparedata[0:4])[0]
	objectId = struct.unpack('<L', sparedata[4:8])[0]
	#print objectId
	chunkId = struct.unpack('<L', sparedata[8:12])[0]
	#print chunkId
	byteCount = struct.unpack('<L', sparedata[12:16])[0]

	'''
typedef struct {
    yaffs_ObjectType type;

        /* The following apply to directories, files, symlinks - not hard links */
        __u32 yst_mode;         /* protection */

    __u32 yst_uid;
    __u32 yst_gid;
    __u32 yst_atime;
    __u32 yst_mtime;
    __u32 yst_ctime;
	'''

	## check if the file is a new file
	if byteCount == 0xffff:
		## new file, so process the chunk data
		## first read in the object header
		chunktype = struct.unpack('<L', chunkdata[0:4])[0]

		## unused checksum, can be ignored
		parentObjectId = struct.unpack('<L', chunkdata[4:8])[0]

		## store the parent id for this object, so it can be retrieved later
		objectparent[objectId] = parentObjectId

		## unused checksum, can be ignored
		checksum = struct.unpack('<H', chunkdata[8:10])[0]

		## extract the name, up to the first '\x00' character
		## and store it
		yaffsname = chunkdata[10:10+YAFFS_MAX_NAME_LENGTH+1+2]
		eoname = yaffsname.find('\x00')
		yaffsname=yaffsname[:eoname]
		objectidtoname[objectId] = yaffsname

		## reconstruct the full path
		if objectId != 1 and objectidtoname.has_key(parentObjectId) and objectId != parentObjectId:
			objectpath = yaffsname
			newparentid = parentObjectId
			while newparentid != 1:
				yaffsname = os.path.join(objectidtoname[newparentid], yaffsname)
				newparentid = objectparent[newparentid]
			print yaffsname

		if chunktype == YAFFS_OBJECT_TYPE_FILE:
			print "CHUNK file"
		elif chunktype == YAFFS_OBJECT_TYPE_SYMLINK:
			print "CHUNK symlink"
		elif chunktype == YAFFS_OBJECT_TYPE_DIRECTORY:
			## create the directory and move on
			print "CHUNK directory"
		elif chunktype == YAFFS_OBJECT_TYPE_HARDLINK:
			print "CHUNK hardlink"
		elif chunktype == YAFFS_OBJECT_TYPE_SPECIAL:
			print "CHUNK special"
		else:
			print "CHUNK unknown"
		pass

	## move on to the next chunk
	bytesread = bytesread + len(chunkdata) + len(sparedata)
