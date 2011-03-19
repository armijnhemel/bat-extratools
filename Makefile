all:	squashfsbroadcom cramfsunpack

squashfsbroadcom:
	cd squashfs-broadcom; make

cramfsunpack:
	cd cramfs; ./configure; make
