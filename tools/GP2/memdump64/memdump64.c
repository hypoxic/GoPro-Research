/*
 * Modified from busybox devmem to read RTOS into a binary.
 *
 * Compile: aarch64-linux-gnu-gcc memdump64.c -o memdump64 -static
 * Usage:   memdump64 <start_address> <size> [output_file]
 *          Addresses and sizes are hex (0x prefix optional).
 *          output_file defaults to /tmp/fuse_d/read.bin
 * Note: busybox devmem 0x40200208 to determine end of RODATA
 */

/*
 * Licensed under GPLv2 or later, see file LICENSE in this source tree.
 *  Copyright (C) 2000, Jan-Derk Bakker (J.D.Bakker@its.tudelft.nl)
 *  Copyright (C) 2008, BusyBox Team. -solar 4/26/08
 */

#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>

#define DEFAULT_OUTPUT		"/tmp/fuse_d/read.bin"
#define nBUFF_ELEMENTS		0x200	/* 32-bit words per write */

static void usage(const char *prog)
{
	fprintf(stderr, "Usage: %s <start_address> <size> [output_file]\n", prog);
	fprintf(stderr, "  start_address, size in hex; output_file defaults to %s\n", DEFAULT_OUTPUT);
	fprintf(stderr, "HERO11: Run devmem 0x40200208 to find out end of RODATA\n");
}

static int parse_hex(const char *s, uint64_t *out)
{
	char *end;

	errno = 0;
	*out = strtoull(s, &end, 16);
	return (errno || end == s || *end != '\0') ? -1 : 0;
}

int main(int argc, char **argv)
{
	uint64_t start, size, remaining;
	const char *filename = DEFAULT_OUTPUT;
	uint32_t rbuf[nBUFF_ELEMENTS];
	volatile uint32_t *src;
	size_t page_size, offset_in_page, mapped_size;
	void *map_base;
	FILE *fw;
	int fd;

	if (argc < 3 || argc > 4) {
		usage(argv[0]);
		return EXIT_FAILURE;
	}

	if (parse_hex(argv[1], &start) || parse_hex(argv[2], &size) || size == 0) {
		fprintf(stderr, "[ERROR] invalid start address or size\n");
		usage(argv[0]);
		return EXIT_FAILURE;
	}
	if (start & 3) {
		fprintf(stderr, "[ERROR] start address must be 4-byte aligned\n");
		return EXIT_FAILURE;
	}
	if (argc == 4)
		filename = argv[3];

	page_size = (size_t)getpagesize();
	offset_in_page = (size_t)(start & (page_size - 1));
	/* Round up to whole 32-bit words */
	size = (size + 3) & ~(uint64_t)3;
	mapped_size = offset_in_page + size;

	printf("Reading [0x%" PRIx64 "]-[0x%" PRIx64 "] (0x%" PRIx64 " bytes) to %s\n",
	       start, start + size, size, filename);

	fd = open("/dev/mem", O_RDONLY | O_SYNC);
	if (fd < 0) {
		perror("open /dev/mem");
		return EXIT_FAILURE;
	}

	map_base = mmap(NULL, mapped_size, PROT_READ, MAP_SHARED, fd,
			(off_t)(start - offset_in_page));
	if (map_base == MAP_FAILED) {
		perror("mmap");
		close(fd);
		return EXIT_FAILURE;
	}

	fw = fopen(filename, "wb");
	if (fw == NULL) {
		fprintf(stderr, "fopen %s: %s\n", filename, strerror(errno));
		munmap(map_base, mapped_size);
		close(fd);
		return EXIT_FAILURE;
	}

	/* Copy with 32-bit volatile reads; device memory may not tolerate memcpy */
	src = (volatile uint32_t *)((char *)map_base + offset_in_page);
	remaining = size / sizeof(uint32_t);
	while (remaining) {
		size_t n = remaining > nBUFF_ELEMENTS ? nBUFF_ELEMENTS : (size_t)remaining;
		size_t i;

		for (i = 0; i < n; i++)
			rbuf[i] = *src++;

		if (fwrite(rbuf, sizeof(uint32_t), n, fw) != n) {
			fprintf(stderr, "fwrite %s: %s\n", filename, strerror(errno));
			fclose(fw);
			munmap(map_base, mapped_size);
			close(fd);
			return EXIT_FAILURE;
		}
		remaining -= n;
	}

	if (fclose(fw) != 0) {
		fprintf(stderr, "fclose %s: %s\n", filename, strerror(errno));
		munmap(map_base, mapped_size);
		close(fd);
		return EXIT_FAILURE;
	}
	munmap(map_base, mapped_size);
	close(fd);

	printf("done\n");
	return EXIT_SUCCESS;
}
