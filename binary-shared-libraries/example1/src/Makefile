.PHONY: all clean
all: example1

clean:
	rm -rf example1 MyCustomCxxLib.so my_custom_c_lib.so

example1: main.cpp MyCustomCxxLib.so MyCustomCxxLib.h my_custom_c_lib.so my_custom_c_lib.h
	g++ -O0 -o $@ main.cpp MyCustomCxxLib.so my_custom_c_lib.so
	strip $@

%.so: %.c
	gcc -shared -O0 -o $@ $^
	strip $@

%.so: %.cxx
	g++ -shared -O0 -o $@ $^
	strip $@
