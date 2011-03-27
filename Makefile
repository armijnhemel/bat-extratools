all:	squashfsbroadcom squashfsopenwrtold cramfsunpack

squashfsbroadcom:
	cd squashfs-broadcom; make

squashfsopenwrtold:
	cd squashfs-openwrt; make

cramfsunpack:
	cd cramfs; ./configure; make
