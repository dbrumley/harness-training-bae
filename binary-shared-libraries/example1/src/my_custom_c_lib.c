#include <stdio.h>

void my_custom_c_lib_process_data(char *buf, int len) {
  // Pretend like this is interesing and meaningful processing.
  // Maybe say we're formatting the buffer data into a human-readable
  // format, and storing it somewhere.

  for(int i = len-1; i >= 0; i--)
    putchar(buf[i] ^ (len - i - 1));
  putchar('\n');
}
