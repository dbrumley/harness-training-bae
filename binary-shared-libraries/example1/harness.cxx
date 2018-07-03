// c++ -o harness harness.cxx MyCustomCxxLib.so my_custom_c_lib.so
#include <stdio.h>

extern int MyCustomCxxLib::process_data(const char*, char*);

// In C++, C functions must be declared extern "C" (this lets C++ know that
// it should link against a symbol with an unmangled name).
extern "C" void my_custom_c_lib_process_data(char*, int);

int main(int argc, char *argv[]) {
  FILE *f = fopen("fuzzfile", "rb");

  //... TODO

  int x = MyCustomCxxLib::process_data(in, out);
  my_custom_c_lib_process_data(out, x);

  return 0;
}
