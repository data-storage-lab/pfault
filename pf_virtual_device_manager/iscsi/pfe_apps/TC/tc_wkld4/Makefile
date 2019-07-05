.PHONY: all clean

all:
	gcc -g -Wall -I/usr/local/include initer.c  \
		tc_wkld4_config.c -o initer.x -L/usr/local/lib \
		-ltokyocabinet -lz -lbz2 -lrt -lpthread -lm -lc
	gcc -g -Wall -I/usr/local/include worker.c  \
		tc_wkld4_config.c -o worker.x -L/usr/local/lib \
		-ltokyocabinet -lz -lbz2 -lrt -lpthread -lm -lc
	gcc -g -Wall -I/usr/local/include checker.c  \
		tc_wkld4_config.c -o checker.x -L/usr/local/lib \
		-ltokyocabinet -lz -lbz2 -lrt -lpthread -lm -lc

clean:
	rm -f *~
	rm -f *.x
	rm -f ./casket.tcb
	rm -f /tmp/casket.tcb
