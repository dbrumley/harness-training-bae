//
// Compile with: c++ -o harness harness.cxx MyCustomCxxLib.so my_custom_c_lib.so
//

#include <stdio.h>
#include <string.h>

namespace MyCustomCxxLib {
  int process_data(const char*, char*);
}

// In C++, C functions must be declared with extern "C".
// This lets C++ know to look for the unmangled name when linking.
extern "C" void my_custom_c_lib_process_data(char*, int);

int main(int argc, char *argv[]) {
  const char *filepath = "./fuzzfile";
  FILE *f = fopen(filepath, "rb");
  if(!f) {
    fprintf(stderr, "error opening %s\n", filepath);
    return 1;
  }

  fseek(f, 0, SEEK_END);
  long size = ftell(f);
  fseek(f, 0, SEEK_SET);
  char *buf = new char[size+1];
  if(fread(buf, size, 1, f) != 1) {
    fprintf(stderr, "error reading %s\n", filepath);
    return 1;
  }
  buf[size] = 0;

  char *out = new char[strlen(buf)+5];
  int x = MyCustomCxxLib::process_data(buf, out);
  my_custom_c_lib_process_data(out, x);

  //delete[] buf;
  //delete[] out;
  return 0;
}
