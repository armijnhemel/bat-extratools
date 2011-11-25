all:	squashfsbroadcom squashfsralink squashfsopenwrtold cramfsunpack unyaffsunpack squashfs42 ddx jds

squashfsbroadcom:
	cd squashfs-broadcom; make

squashfsralink:
	cd squashfs-ralink; make

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
	mv dedexer/jdeserialize.jar jdeserialize/bat-jdeserialize.jar
