#include <string.h>

namespace mylib {
  int totally_legit_and_not_trivially_exploitable_function(const char *data) {
    char stackbuf[32];
    int len = *(int*)data;
    if(len < 32) { // bug: negative length passes...
      strncpy(stackbuf, data+4, len); // ...and gets interpreted as large unsigned
      return 0;
    } else {
      return 1;
    }
  }
}
