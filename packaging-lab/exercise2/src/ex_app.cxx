#include "mylib.hxx"
#include "pugixml.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pcre.h>
#include <libgen.h>

bool pcre_find(const char *regex, const char *buf) {
  const char *pcreErrorStr;
  int pcreErrorOffset;
  pcre *reCompiled = pcre_compile(regex, 0, &pcreErrorStr, &pcreErrorOffset, NULL);
  if(reCompiled == NULL) {
    printf("ERROR: pcre: %s\n", pcreErrorStr);
    exit(1);
  }
  int sub;
  int ret = pcre_exec(reCompiled, NULL, buf, strlen(buf), 0, 0, &sub, 1);
  if(ret < 0) {
    return false;
  } else {
    return true;
  }
}

pugi::xml_node get_one(pugi::xml_node &root, const char *query) {
  pugi::xpath_node_set x = root.select_nodes(query);
  if(x.empty()) {
    fprintf(stderr, "failed to find %s\n", query);
    exit(1);
  }
  return x.first().node();
}

int main(int argc, char *argv[]) {
  pugi::xml_document doc;

  if(!(getenv("EAPP_RESOURCES") && getenv("CONFIG_XML"))) {
    fprintf(stderr, "missing env var(s)\n");
    return 1;
  }
  pugi::xml_parse_result result = doc.load_file(getenv("CONFIG_XML"));
  if(!result) {
    fprintf(stderr, "failed to load config xml\n");
    return 1;
  }

  if(strcmp(get_one(doc, "/config/key").text().get(), "value") != 0) {
    fprintf(stderr, "wrong value for config key\n");
    return 1;
  }

  char *pwd = dirname(getenv("CONFIG_XML"));
  strcat(pwd, "/");
  const char *target = get_one(doc, "/config/import").text().get();
  strcat(pwd, target);

  result = doc.load_file(pwd);
  if(!result) {
    fprintf(stderr, "failed to load config aux xml and instead loaded %s\n",pwd);
    return 1;
  }

  bool need_foo=true, need_bar = true;
  for(pugi::xpath_node node: doc.select_nodes("/config/resource")) {
    char buf[128];
    strncpy(buf, getenv("EAPP_RESOURCES"), 127);
    strncat(buf, "/", 127);
    strncat(buf, node.node().text().get(), 127);
    buf[127] = 0;
    FILE *f = fopen(buf, "r");
    if(!f) {
      fprintf(stderr, "missing resource %s\n", buf);
      continue;
    }
    memset(buf, 0, 128);
    fread(buf, 1, 128, f);
    fclose(f);
    if(pcre_find("mag[ic][ic] foo", buf)) need_foo = false;
    if(pcre_find("mag[ic][ic] bar", buf)) need_bar = false;
  }

  if(need_foo || need_bar) {
    fprintf(stderr, "failed to load resources\n");
    return 1;
  }

  if(argc < 3 || strcmp(argv[1], "run") != 0) {
    fprintf(stderr, "Usage: %s run paths...\n", argv[0]);
    return 1;
  }

  {
    FILE *f = fopen("/etc/ex_app_config", "r");
    if(!f) {
      fprintf(stderr, "missing the global config file /etc/ex_app_config!\n");
      return 1;
    }
    fclose(f);
  }

  for(int i = 2; i < argc; ++i) {
    FILE *f = fopen(argv[i], "r");
    if(!f) {
      fprintf(stderr, "failed to open %s\n", argv[i]);
      return 1;
    }
    char buf[64];
    size_t x = fread(buf, 1, 63, f);
    if(x > 0) {
      buf[x] = 0;
      int y = mylib::totally_legit_and_not_trivially_exploitable_function(buf);
      fprintf(stderr, "%d\n", y);
    } else {
      fprintf(stderr, "read nothing from %s\n", argv[i]);
    }
    fclose(f);
  }

  fprintf(stderr, "Done!\n");
}
