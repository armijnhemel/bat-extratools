all:	bat-simg2img

libsparse_files := backed_block.o output_file.o sparse.o sparse_crc32.o sparse_err.o sparse_read.o

%.o: %.c
	$(CC) -Iinclude -c $< -o $@

libsparse.a: $(libsparse_files)
	$(AR) r $@ $^

bat-simg2img: simg2img.o libsparse.a
	$(CC) -o $@ $< -I. -L. -lsparse -lz

clean:
	$(RM) *.o *.a bat-simg2img
