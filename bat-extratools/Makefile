all:	squashfsbroadcom squashfsralink squashfsrealtek squashfsatheros squashfsatheros2 squashfsopenwrtold squashfsddwrt squashfs42 cramfsunpack

squashfsbroadcom:
	cd squashfs-broadcom; make

squashfsralink:
	cd squashfs-ralink; make

squashfsrealtek:
	cd squashfs-realtek/squashfs-tools; make

squashfsatheros:
	cd squashfs-atheros; make

squashfsatheros2:
	cd squashfs-atheros2; make

squashfsopenwrtold:
	cd squashfs-openwrt; make

squashfsddwrt:
	cd squashfs-ddwrt; make

squashfs42:
	cd squashfs4.2/squashfs-tools; make

cramfsunpack:
	cd cramfs; ./configure --without-ncurses; make
	mv cramfs/disk-utils/fsck.cramfs cramfs/disk-utils/bat-fsck.cramfs

#unyaffsunpack:
#	cd unyaffs; make
