// harness-collapse.cpp
#include "tinyxml2.h"

int main(int argc, char **argv)
{
    tinyxml2::XMLDocument doc(true, COLLAPSE_WHITESPACE);
    doc.LoadFile( argv[1] );
    doc.Print();
    int errorID = doc.ErrorID();

    return errorID;
}
