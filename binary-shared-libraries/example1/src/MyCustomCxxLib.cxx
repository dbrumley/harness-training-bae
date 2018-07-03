namespace MyCustomCxxLib {

int process_data(const char *in, char *out) {
  // Pretend like this is interesing and meaningful processing.
  // Let's say we're gathering sensor readings from 'in', and normalizaing
  // them or whatever into 'out'.

  char buf[100];

  int i = 0;

  char *tmp = &buf[0];
  while(*in)
    *tmp++ = *in++ ^ i++;

  for(int j = 0; j < i; j++)
    out[j] = buf[i - j - 1];

  return i;
}

}
