## Writing a Simple Harness with Source Code

### Intro

The simplest kind of source-based harness to write is for a target that has an
obvious entry point, as is often the case for parsers.  Having source is a big
advantage, and beaing able to write a custom harness gives a lot of control
over what you can test effectively, especially when the target is a library.

This lab will take you through writing a very simple harness for an XML library
whose source is freely available, tinyxml2.  We will demonstrate using a custom
harness to both fuzz the main entry point for the library as well as a specific
function in the library.

### First Steps

First you have to download the code and unzip the code, as shown below.

```
curl -o tinyxml2-2.0.1.tar.gz https://codeload.github.com/leethomason/tinyxml2/tar.gz/2.0.1
# or grab the latest and ignore the talk of finding bugs
#curl -o tinyxml2-6.2.0.tar.gz https://codeload.github.com/leethomason/tinyxml2/tar.gz/6.2.0
tar xzf tinyxml2-2.0.1.tar.gz
cd tinyxml2-2.0.1/
```

If you look around in that directory, you'll see that there aren't a whole lot
of files, which is really helpful when you're trying to figure out where to
start!

### Writing The Simplest Harness

By reading the docs or the code itself, we can find that this library has a
pretty straightforward interface for either loading from a file or from a char
array, which makes writing a harness to the parser very simple.

Open `tinyxml2.cpp` (or `xmltest.cpp`) and look for the relevant functions for
loading a file for parsing (or parsing a char array into an XML object).  We'll
want to instantiate the most high-level object and pass fuzz input to it, which
we will get from the file whose name is accessible to the harness as argv[1].

Optionally, you should print the object out or somehow confirm that the library
successfully parsed the content you passed to it. This library provides
functionality to print out XML objects, but you should at least return 0 on a
successful parse and something else if something went wrong.


```
// harness.cpp
#include "tinyxml2.h"

int main(int argc, char **argv)
{
    int retval = 0;
    // Your code goes here
    // TODO: Instantiate basic XML object
    // TODO: Parse content of argv[1] into XML object
    // TODO: Print the XML object or confirm parsing

    return retval;
}
```

### Building the Harness

Now we just have to compile the harness with the target library code
linked in, which is easy in the case of this library, it's just:

```
g++ tinyxml2.cpp harness.cpp -o harness
```

You should test your compiled code on files that are valid XML and ones that
are not valid XML.

### Packaging for Mayhem

Now we create a package for uploading to mayhem. Type `mayhem package` to see
what options the command takes, but we recommend using -o as in the invocation
below.

```
mayhem package -o /tmp/tinyxml2-harness/ harness
```

Optionally, give an actual XML file as an initial seed by copying the file into
the `corpus` directory in the root of your package directory.  Mayhem would
work even without this, but because this parser will discard things that don't
look like XML, it speeds up the process to start with a valid XML file (even if
the contents were as simple as `<a></a>`).  Supplying a test case is done as
shown below:

```
cp resources/utf8test.xml /tmp/tinyxml2-harness/corpus/
```

Then upload the package and use the `--start-sword` option to start testing!

```
mayhem upload /tmp/tinyxml2-harness/ --start-sword
```

If you used tinyxml2 version 2.0.1, you will probably see a crash (though it
probably isn't a very exciting one) and can look at the output for that.
Otherwise, it might be interesting to download a couple of the generated
testcases and see what kind of inputs Mayhem generated.

### Next Steps with Source

So at this point we're hitting the parsing functionality of the library, which
touches a good bit of code, but it's also likely the most battle-tested part of
the codebase.  Some ideas for further testing would be to use the library to
manipulate the XML or to turn on some non-default options, so let's work
through the latter option.

Fire back up your text editor and change the XMLDocument constructor to use a
non-default option (there's only two options and only one sounds like it would
do more processing rather than less on the inputs).  Then compile your code
with a new output filename and use the sample XML file below to demonstrate
that the non-default option makes a difference.

```
<a> This 
	is &apos;  text  &apos; </a>
<b>  This is &apos; text &apos;  
</b>
<c>This  is  &apos;  
       
	text &apos;</c>
</element>
```

Once you've confirmed a difference between the new harness and the previous
version, you should package and upload the new binary.  You should also upload
the above XML sample as a seed to help speed the process of hitting the code
the new harness is designed to test.  Refer to the previous examples and try
this now.

While you aren't likely to find a crash, and encouraging indication that you
are hitting new code would be to see a higher number of edges covered at the
end of the run.

### Fuzzing a Specific Function

One of the biggest benefits of having source code available is that you can
more easily understand the code base and zero in on specific functions to fuzz.
Picking specific functions to fuzz is made easier by the fact that you can
see how a target function is called in the codebase, and potentially modify the
code to make it easier to fuzz.

If you used version 2.0.1 for the earlier parts of the lab, you probably came
across a crash in `StrPair::GetStr()` (if you didn't, you can still look at the
code and follow the same process).  If you then started looking at the function
to see if there were any interesting pieces of it, you might notice that it
calls a utility function `XMLUtil::GetCharacterRef()`.  This function may not
be the cause of the crash you saw earlier, but it can still be an interesting
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
understood just by looking around the function ("p" is the name of the pointer
to the XML string throughout the codebase, and the other two are initialized
right next to the call).  The reason I say it's important to understand how a
function is called is because you might cause a crash by supplying invalid
arguments for `buf` and `len`, but any such bugs wouldn't be of practical value
because they wouldn't be reachable from the normal functionality of the
library.

If we look at the function itself, we can see that it only references local
variables and the arguments, so we don't need to worry about initializing any
global state (a good bonus!).  And since two out of the three arguments are set
before the only call to the function, we really just need to pass in fuzz data,
which is only a little bit different than the previous examples because we'd
like need to read data from the file and pass it to the function.

````
// gcr-harness.cpp
#include <unistd.h>
#include <fcntl.h>
#include "tinyxml2.h"

using namespace tinyxml2;

int fuzz_gcr(char *p, ssize_t length) {

    // Your code goes here
    // set up any local variables
    // Call GetCharacterRef() with the fuzz data

    return 0;
}

int main(int argc, char **argv) {

    // Your code goes here
    // Declare a local buffer
    // open argv[1]
    // read a reasonable number of bytes from the opened file
    // call fuzz_gcr() with the data read from the file

    return 0;
}
```

### Improving the Harness

Now you could compile this harness and upload it like you did the previous, but
we could also take a look around the target function and gain some insight that
will help improve our fuzzing.

If you notice there are two if-conditions that must be true in order for
`GetCharacterReference()` to be called. So try taking these into account and
modify the harness to mirror the conditions needed for the target function to
get called in normal circumstances. This will guarantee that our fuzz inputs
don't get discarded unnecessarily (since `GetCharacterReference()` also checks
for one of the two conditions before doing anything interesting) and also makes
sure that our inputs would make it to the target function if we were to pass
them in the normal parsing process.

Once you've made your modifications, package and upload the new compiled
harness. You will probably see a faster taper in terms of new testcases because
there isn't much code that is reachable from the target function, but you
should see more than just one testcase in a big cliff (which would be and
indication that something isn't right).

### Conclusion

At this point, we've written a custom harness for both the main functionality
of the tinyxml2 library and a custom harness to target a specific helper
function.  This lab shows some of these advantages of having source, like how
it is easier to understand how certain functions are used and whether or not
there are global dependencies for targeted functions.

We didn't touch on some of the advanced topics that are possible with source
(i.e. patch out checks, instantiate complicated objects, or redirect inputs)
but this should give you an idea of the power and convenience of being able to
harness source code.

