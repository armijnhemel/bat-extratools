all:	squashfsbroadcom squashfsralink squashfsatheros squashfsopenwrtold squashfs42 cramfsunpack unyaffsunpack ddx jds

squashfsbroadcom:
	cd squashfs-broadcom; make

squashfsralink:
	cd squashfs-ralink; make

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

ddx:
	ant -f dedexer/build.xml
	mv dedexer/ddx.jar dedexer/bat-ddx.jar

jds:
	ant -f jdeserialize/build.xml
	mv jdeserialize/jdeserialize.jar jdeserialize/bat-jdeserialize.jar
