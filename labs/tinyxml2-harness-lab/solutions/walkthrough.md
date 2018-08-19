## Harnessing tinyxml2

### Intro

The simplest kind of source-based harness to write is for a library that has an
obvious entry point, as is often the case for parsers.  This lab will take you
through writing a very simple harness for an XML library, tinyxml2.

### First Steps

First you have to download the code and unzip the code, as shown below.

```
curl -o tinyxml2-2.0.1.tar.gz https://codeload.github.com/leethomason/tinyxml2/tar.gz/2.0.1
# or grab the latest and ignore the talk of finding bugs
#curl -o tinyxml2-6.2.0.tar.gz https://codeload.github.com/leethomason/tinyxml2/tar.gz/6.2.0
tar xzf tinyxml2-6.2.0.tar.gz
cd tinyxml2-6.2.0/
```

If you look around in that directory, you'll see that there aren't a whole lot
of files, which is really helpful when you're trying to figure out where to
start!

### Writing The Simplest Harness

By reading the docs or the code itself, we can find that this library has a
pretty straightforward interface for either loading from a file or from a char
array, which makes writing a harness to the parser very simple.

Open up a C++ file (with `vim harness.cpp` or your favorite text editor) and 
type in the following code:

```
// harness.cpp
#include "tinyxml2.h"

int main(int argc, char **argv)
{
    tinyxml2::XMLDocument doc;
    doc.LoadFile( argv[1] );
    doc.Print();
    int errorID = doc.ErrorID();

    return errorID;
}
```

### Building the harness

Now we just have to compile the harness with the target library code 
linked in, which is easy in the case of this library, it's just:

```
g++ tinyxml2.cpp harness.cpp -o harness
```

Feel free to test the code on files that are valid XML (or not).
```
./harness resources/dream.xml ; echo $?
./harness resources/empty.xml ; echo $?
./harness ; echo $?
```

### Packaging for Mayhem

Now we create a package for uploading to mayhem:

```
mayhem package -o /tmp/tinyxml2-harness/ harness
```

Optionally, give an actual XML file as an initial seed

```
cp resources/utf8test.xml /tmp/tinyxml2-harness/corpus/
```

Then upload the package to start testing!

```
mayhem upload /tmp/tinyxml2-harness/ --start-sword
```

### Next Steps with source

So at this point we're hitting the parsing functionality of the library, which
touches a good bit of code, but it's also likely the most battle-tested part of
the codebase.  Some ideas for further testing would be to use the library to
manipulate the XML or to turn on some non-default options, the simplest of
which I've shown below.

Fire back up your text editor and change the XMLDocument constructor to use a
non-default option, then type in the sample XML file to show this difference.

```
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
```

whitespace-test.xml contents:

```
<a> This 
	is &apos;  text  &apos; </a>
<b>  This is &apos; text &apos;  
</b>
<c>This  is  &apos;  
       
	text &apos;</c>
</element>
```

Now build and test that the new harness exhibits different behavior. 

```
g++ tinyxml2.cpp harness-collapse.cpp -o harness-collapse
./harness whitespace-test.xml
./harness-collapse whitespace-test.xml
```

Now let's package and upload the new harness:

```
mayhem package -o /tmp/tinyxml2-collapse-harness/ harness-collapse-print 
# optionally, include any XML files as seeds between these commands
mayhem upload /tmp/tinyxml2-collapse-harness/ --start-sword
```

If you wanted to upload the whitespace-collapsing XML sample as a seed, that
would help speed the process of hitting the code the new harness is designed 
to test.  Use the new file and the previous examples to give that a try.

At this point, you've written a simple source-based harness, but you should
also have an idea of some of the limitations of this and the parts of the 
target library that this simple harness will not be able to test.

### Picking a Target Function

One of the biggest benefits of having source code available is that you can
more easily understand the code base and zero in on specific functions to fuzz.
Picking specific functions to fuzz is made easier by the fact that you can
see how a target function is called in the codebase, and potentially modify the
code to make it easier to fuzz.

If you used version 2.0.1 for the earlier parts of the lab, you probably came
across a crash in StrPair::GetStr() (if you didn't, you can still look at the
code and follow the same process.  If you then started looking at the function
to see if there were any interesting pieces of it, you might notice that it
calls a utility function XMLUtil::GetCharacterRef().  This function may not be
the cause of the crash you saw earlier, but it can still be an interesting 
target to fuzz due to its proximity to problem code that is invoked from the
main entry point to the parsing code.

### Harnessing the Target Function

The first thing we need to do is understand how the target function is called
and if it relies on any global state that is outside the scope of the function.
In this case understanding how it is called is very easy because it is only
called in one place in the entire codebase:

tinyxml2.cpp (version 2.0.1):

```
217:    char buf[10] = { 0 };
218:    int len;
219:    p = const cast<char*>( XMLUtil::GetCharacterRef( p, buf, &len ) );
```

What's nice about this usage is that the meaning of the arguments can be
understood just by looking around the function ("p" is the pointer to the XML
string throughout the codebase, and the other two are initialized right next to
the call).  The reason I say it's important to understand how a function is 
called is because you could cause a crash by supplying invalid arguments for
`buf` and `len`, but any bugs wouldn't be of practical value because they
wouldn't be reachable from the normal functionality of the library.

If we look at the function itself, we can see that it only references local
variables and the arguments, so we don't need to worry about initializing any
global state (a good bonus!).  And since two out of the three arguments are set
before the only call to the function, we really just need to pass in fuzz data,
which is a little bit different than the previous examples because we'd like
to read data from the file and pass it to the function.

gcr-harness.cpp:

````
#include <unistd.h>
#include <fcntl.h>
#include "tinyxml2.h"

using namespace tinyxml2;

int fuzz_gcr(char *p, ssize_t length) {
    char buf[10] = { 0 };
    int len = 0;
    char* adjusted = const_cast<char*>( XMLUtil::GetCharacterRef( p, buf, &len ) );
    
    return 0;
}
    
int main(int argc, char **argv) {
    const size_t bufsize = 20;
    char buf[bufsize+1] = {0};
	int fd = open(argv[1], 0);
    ssize_t bytes_read = read(fd, buf, bufsize);
    if (bytes_read > 0) {
        fuzz_gcr(buf, bytes_read);
    }
    
    return 0;
}
```

### Improving the Harness

Now you could compile this harness and upload it like you did the previous, but
we could also take a look around the target function and gain some insight that
will help improve our fuzzing.  

If you notice there are two if-conditions that must be true in order for 
GetCharacterReference() to be called, basically: `*p == '&'` and 
`*(p+1) == '#'`. So with these in mind, we can modify our harness to mirror the
conditions needed for the target function to get called in normal circumstances
and we will guarantee that our fuzz inputs aren't getting discarded 
unnecessarily (since GetCharacterReference() also checks for the '#' before
doing anything interesting).

```
#include <unistd.h>
#include <fcntl.h>
#include "tinyxml2.h"

using namespace tinyxml2;

int fuzz_gcr(char *p, ssize_t length) {
    *p = '&';
    *(p+1) = '#';
    char buf[10] = { 0 };
    int len = 0;
    char* adjusted = const_cast<char*>( XMLUtil::GetCharacterRef( p, buf, &len ) );
    
    return 0;
}
    
int main(int argc, char **argv) {
    const size_t bufsize = 20;
    char buf[bufsize+1] = {0};
	int fd = open(argv[1], 0);
    ssize_t bytes_read = read(fd, buf+2, bufsize-2); // "&#" will be p[0], p[1]
    if (bytes_read > 0) {
        fuzz_gcr(buf, bytes_read);
    }
    
    return 0;
}
```

Now try compiling, packaging, and uploading this code.

Technically we didn't have to do anything like patch out checks, instantiate
complicated objects, or redirect inputs, but this should give you an idea of
the convenience of being able to harness source code.
