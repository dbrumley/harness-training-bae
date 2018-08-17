#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>
#include <pwd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>

void process_buf(char* buf) {
  int i;

  if (buf[0] == 'M') {
    puts("MAGIC");
  }
  if ( *((int*)buf) == 123 ) {
    puts("ABC");
  }

  for (i = 0; i < 1024; i++) {
    if (buf[i] == '.') {
      puts("...");
    }
  }

  if (buf[buf[0]] == buf[1]) {
    puts("FUN");
  }
}

void main(int argc, char** argv) {
  if (argc < 2) {
    printf("Usage: %s config_file_path\n", argv[0]);
    return;
  }

  char* username = getenv("USER");
  if (username == NULL) {
    printf("Missing USER env variable!\n");
    return;
  }

  struct passwd *p = getpwnam(username);
  if (p == NULL) {
    printf("Could not find info for user %s!\n", username);
    return;
  }

  printf("Running as uid=%d\n", p->pw_uid);

  FILE* conf = fopen(argv[1], "r");
  if (conf == NULL) {
    printf("Could not read file %s\n", argv[1]);
    return;
  }

  int port = 0;
  fscanf(conf, "port = %d", &port);
  if ((port <= 1024) || (port >= 65536)) {
    printf("Need to specify 1024 < port < 65536 in config!\n");
    return;
  }

  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    printf("Failed to allocate socket\n");
    return;
  }

  if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int)) < 0) {
    printf("setsockopt(SO_REUSEADDR) failed\n");
    return;
  }

	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_port = htons((unsigned short) port);
	inet_pton(AF_INET, "127.0.0.1", &(addr.sin_addr));
	if(bind(sockfd, (struct sockaddr*) &addr, sizeof(addr)) < 0) {
    printf("failed to bind to port %d on localhost, exiting\n", port);
    return;
	}
	listen(sockfd, 3);
	int socklen = sizeof(addr);
	while(1) {
    int accfd = accept(sockfd, (struct sockaddr*) &addr, &socklen);
    if (accfd < 0) {
        printf("Accept failed! returned %d, strerror %s\n", accfd, strerror(errno));
        return;
    }

    char buf[1024];
    FILE* welcome = fopen("welcome.txt", "r");
    int welcome_len = fread(buf, 1, 1024, welcome);
    write(accfd, buf, welcome_len);

    int status = read(accfd, &buf, 1024);

    process_buf(buf);

    close(accfd);
	}
  return;
}
