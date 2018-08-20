#include <string.h>
#include <map>
#include <string>

//
// In this particular case, the exact sizes don't matter
// and over-approximations are fine. However, in other scenarios
// (particularly when custom objects are used inside arrays or
// std::vectors), you must reverse-engineer to find a correct size.
//

class CustomClassA {
  char space[100];
public:
  CustomClassA();
};

class CustomClassB {
  char space[100];
public:
  CustomClassB(CustomClassA*, std::map<int, std::string> const&);
  int harness_me(char*, int);
};

int main(int argc, char *argv[]) {
  CustomClassA a;
  std::map<int, std::string> m;
  CustomClassB b(&a, m);
  return b.harness_me(argv[1], strlen(argv[1]));
}
