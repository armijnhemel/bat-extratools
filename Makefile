all:	squashfsbroadcom squashfsralink squashfsrealtek squashfsatheros squashfsopenwrtold squashfs42 cramfsunpack unyaffsunpack

squashfsbroadcom:
	cd squashfs-broadcom; make

squashfsralink:
	cd squashfs-ralink; make

squashfsrealtek:
	cd squashfs-realtek/squashfs-tools; make

squashfsatheros:
	cd squashfs-atheros; make

squashfsopenwrtold:
	cd squashfs-openwrt; make

squashfs42:
	cd squashfs4.2/squashfs-tools; make

cramfsunpack:
	cd cramfs; ./configure --without-ncurses; make
	mv cramfs/disk-utils/fsck.cramfs cramfs/disk-utils/bat-fsck.cramfs

unyaffsunpack:
	cd unyaffs; make
