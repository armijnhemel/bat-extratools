#!/usr/bin/python

import sys, os, os.path, struct, tempfile

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

unpackdir = tempfile.mkdtemp()

image_file.seek(0)
bytesread = 0

yaffs2filesize = os.stat('yaffs2_1.img').st_size

if yaffs2filesize%(CHUNK_SIZE + SPARE_SIZE) != 0:
	## this is not a valid yaffs2 file for this chunk size and spare size
	sys.exit(1)

objectidtoname = {}
objectparent = {}

outfile = None

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

	## check if the file is a new file
	if byteCount == 0xffff:
		if outfile != None:
			outfile.close()
		offset = 0
		oid = objectId
		## new file, so process the chunk data
		## first read in the object header
		chunktype = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		## unused checksum, can be ignored
		parentObjectId = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		## store the parent id for this object, so it can be retrieved later
		objectparent[objectId] = parentObjectId

		## unused checksum, can be ignored
		checksum = struct.unpack('<H', chunkdata[offset:offset+2])[0]
		offset = offset + 2

		## extract the name, up to the first '\x00' character
		## and store it
		yaffsname = chunkdata[offset:offset+YAFFS_MAX_NAME_LENGTH+1+2]
		eoname = yaffsname.find('\x00')
		yaffsname=yaffsname[:eoname]
		objectidtoname[objectId] = yaffsname
		offset = offset + YAFFS_MAX_NAME_LENGTH + 1 + 2

		## reconstruct the full path
		if objectId != 1 and objectidtoname.has_key(parentObjectId) and objectId != parentObjectId:
			objectpath = yaffsname
			newparentid = parentObjectId
			while newparentid != 1:
				yaffsname = os.path.join(objectidtoname[newparentid], yaffsname)
				newparentid = objectparent[newparentid]
			print "unpacking", yaffsname

		yst_mode = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		yst_uid = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		yst_gid = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		yst_atime = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		yst_mtime = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		yst_ctime = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		fileSize = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		equivalentObjectId = struct.unpack('<L', chunkdata[offset:offset+4])[0]
		offset = offset + 4

		## extract the alias, up to the first '\x00' character
		## and store it
		aliasname = chunkdata[offset:offset+YAFFS_MAX_ALIAS_LENGTH+1]
		eoname = aliasname.find('\x00')
		if eoname != -1:
			aliasname = aliasname[:eoname]
		else:
			aliasname = None
		offset = offset + YAFFS_MAX_ALIAS_LENGTH + 1

		if chunktype == YAFFS_OBJECT_TYPE_FILE:
			outname = os.path.join(unpackdir, yaffsname)
			outfile = open(outname, 'wb')
		elif chunktype == YAFFS_OBJECT_TYPE_SYMLINK:
			if aliasname != None:
				symlink = os.path.join(unpackdir, yaffsname)
				os.symlink(aliasname, symlink)
		elif chunktype == YAFFS_OBJECT_TYPE_DIRECTORY:
			## create the directory and move on
			createdir = os.path.join(unpackdir, yaffsname)
			try:
				os.makedirs(createdir)
			except:
				pass
		elif chunktype == YAFFS_OBJECT_TYPE_HARDLINK:
			print "CHUNK hardlink"
		elif chunktype == YAFFS_OBJECT_TYPE_SPECIAL:
			print "CHUNK special"
		else:
			print "CHUNK unknown"
		pass
	else:
		## block with data
		outfile.write(chunkdata[:byteCount])

	## move on to the next chunk
	bytesread = bytesread + len(chunkdata) + len(sparedata)

if outfile != None:
	outfile.close()
