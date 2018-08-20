#include <string.h>
#include <iostream>
#include <ex2lib.hxx>

int main(int argc, char *argv[]) {
  if(argc < 2) {
    std::cerr << "need an arg" << std::endl;
    return -1;
  }

  initialization_func();

  CustomClassA *a = new CustomClassA();

  std::map<int, std::string> m;
  m[1338] = "foo";
  m[1339] = "bar";
  m[1340] = "baz";

  CustomClassB *b = new CustomClassB(a, m);

  return b->harness_me(argv[1], strlen(argv[1]));
}
