all:	squashfsbroadcom squashfsopenwrtold cramfsunpack unyaffsunpack

squashfsbroadcom:
	cd squashfs-broadcom; make

squashfsopenwrtold:
	cd squashfs-openwrt; make

cramfsunpack:
	cd cramfs; ./configure; make

unyaffsunpack:
	cd unyaffs; make
