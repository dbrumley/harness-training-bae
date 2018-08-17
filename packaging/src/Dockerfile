FROM debian:jessie-slim

RUN apt-get -y update && apt-get -y install build-essential cmake libpcre3-dev

WORKDIR /root

#COPY https://github.com/zeux/pugixml/archive/v1.9.tar.gz .
COPY pugixml-1.9.tar.gz ./
RUN tar -xf pugixml-1.9.tar.gz && \
    cd pugixml-1.9 && \
    printf '#define PUGIXML_NO_STL\n#define PUGIXML_NO_EXCEPTIONS\n#define PUGIXML_HAS_LONG_LONG\n' > src/pugiconfig.hpp && \
    printf '\nset_target_properties(pugixml PROPERTIES OUTPUT_NAME "myxml")' >> CMakeLists.txt && \
    mkdir build && \
    cd build && \
    cmake .. -G 'Unix Makefiles' -DBUILD_SHARED_LIBS=1 && \
    make && \
    ls -l && \
    mv libmyxml.so* /root/

COPY ex_app/ ./ex_app/
COPY ex_app.cxx mylib.cxx mylib.hxx ./

RUN c++ -std=c++11 -fno-stack-protector -shared -fPIC mylib.cxx -o libmylib.so && \
    c++ -std=c++11 -fno-stack-protector -I/root/pugixml-1.9/src ex_app.cxx /root/libmyxml.so.1.9 libmylib.so -lpcre -o ex_app.exe && \
    ldd ex_app.exe && \
    mv /root/libmyxml.so* libmylib.so ex_app/libs/ && \
    mv ex_app.exe ex_app/ex_app && \
    chmod a+x ex_app/ex_app ex_app/run.sh

RUN touch /etc/ex_app_config && \
    ./ex_app/run.sh /dev/null && \
    printf '\4\0\0\0AAAAAAAA'   > /tmp/test && ./ex_app/run.sh /tmp/test && \
    printf '\4\377\0\0AAAAAAAA' > /tmp/test && ./ex_app/run.sh /tmp/test && \
    { printf '\1\1\1\377%0100d' 1 > /tmp/test && ./ex_app/run.sh /tmp/test || true; } && \
    echo 'if it says "read nothing ; done ; 0 ; done ; 1 ; done ; segfault", it worked'
