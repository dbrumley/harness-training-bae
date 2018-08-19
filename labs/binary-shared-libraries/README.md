## Binary-only Shared Library Harnessing

In this lab, we'll look at "binary-only" C++ applications that do not seem immediately amenable to harnessing.

In order to fuzz these applications anyways---or at least, parts of them---we'll harness libraries shipped with the application. We'll use a strategy of linking a source C++ harness against the binary.

### Background

#### (What's a shared library again?)

* .dll on Windows; .so on Linux
* Contains compiled code, and associated data
* Different programs can use the same shared libraries

The original purpose of shared libraries is to save disk space, by sharing compiled code between multiple binary programs. When a software library is compiled as a shared library object, programs can load this library instead of containing their own copy of the library's code. (Note that programs loading a library make a virtual in-memory copy of that library; so, multiple programs sharing the same shared library don't interfere with each other.)

Shared libraries can also be used to provide software libraries in a pre-compiled form, and without necessarily including their full source. In this use case, header files are provided as well. These header files tell the source compiler how to link against the shared library. There is also program metadata within shared libraries themselves containing linking information, most notably function name symbols.

Modern applications are often delivered in a package consisting of one or more program executables, and multiple shared libraries that the programs depend upon. In this use case, the shared libraries may not actually be intended to be shared among multiple programs, or have new programs linked against them. But it remains technically possible... and we're about to do it.

#### Harnessing libraries vs applications.

In general, when harnessing any library-like component of an application (not just shared libraries), consider the following:

The bad news:

* A harness for a library is essentially an alternate application written with that library. Even though this alternate application can be simple, creating it is often more work than fuzzing an existing application.
* The way an application uses (or misuses) a library may differ from the way a harness uses that library. A harness that does not adequately imitate the application will miss or encounter different bugs.
* And obviously, a library harness has no ability to find bugs in application code outside of that library.

There are two main reasons you may wish to harness a library, as opposed to an application:

* The library may be easier to harness than the application. For example, an HTML parser is relatively easy to harness, and a web browser is not.
* Potentially improving the speed or quality of fuzzing: At the library level, your harness can have a more fine-grained ability to skip slow or uninteresting parts of the software logic, resulting in a faster harness that finds more bugs.

Typically speaking, it's best to try to harness a whole application first, along with any library components you believe are particularly easy and particularly buggy (for example, parsers or protocol-processing code). Additional library components should be harnessed only if the whole-application harness doesn't seem to be producing adequate coverage for that component.

#### Binary-only

A large part of the difficulty in harnessing binary-only applications is that---unless the application is trivially harnessable---it often requires reverse-engineering to figure out what to harness, and something like binary patching to implement the harness. Harnessing just the shared libraries of an application provided in binary-only form skirts these difficulties, because usually the whole point of a software library is to provide convenient and flexible ways to programmatically exercise its functionality.

For clarification: this tutorial is aimed at exploring _custom_ shared libraries shipped with an application for which source is not available. If, for example, you know that an application uses an open source library, it's better to acquire the source (preferably for the same version as the application uses) and use source-harnessing techniques on that.

### Requirements

* Skills: Basic C/C++ programming
* Tools: g++ (and gnu binutils)

This tutorial is for C and C++ libraries. Many details and techniques will be specific to C and C++. Although this tutorial uses Linux, and the exact commands shown will only work on Linux, all the principles and tricks here translate to any platform that supports shared libraries---Windows, Mac OS, iOS, Android and more---albeit with different tools and commands.

### Example 1: Basics

This is a toy program that makes unnecessary use of custom shared libraries to merely echo its command line args back to stdout.

Note that "example1" is a C++ program, using one C++ library "MyCustomCxxLib.so" and one C library "my_custom_c_lib.so". Feel free to look at the source before going through the exercise.

Below is a strategy for harnessing these shared libraries. Physically follow along with these steps.

1. Determine what functions the shared libraries offer, and which of these the application is actually using. You may use a reverse engineering program like IDA if you wish, but binutils is sufficient for this one:

    `nm -D example1 MyCustomCxxLib.so my_custom_c_lib.so | c++filt`

    `nm -D` shows us the imported and exported symbols of ELF objects. A `U` sits next to imported symbols, and a `T` sits next to exported function symbols. (If you usually use binutils `nm` without a `-D`, that sometimes works too, but technically this lists the _debug_ symbols in an ELF object instead of the imported & exported symbols. ELFs may have had their debug symbols stripped, as is the case here.)

    `c++filt` is a program that [un-mangles C++ names](https://en.wikipedia.org/wiki/Name_mangling#C++) it sees. The net effect of C++ name mangling is that shared libraries reveal the argument types for C++ functions (e.g. `MyCustomCxxLib::process_data(char const*, char*)` here), but you don't get argument types for C functions (e.g. `my_custom_c_lib_process_data` here).

2. Decide which functions we'd like to call in our harness, and in which order. Typically, this is achieved by mild reverse-engineering of the application or libraries, to find example sequences of how the target functions are being called.

    This isn't a reverse-engineering tutorial, so if you aren't already comfortable with reverse engineering, just open main.cpp. For this program, our harness should pass the output of `MyCustomCxxLib::process_data()` to `my_custom_c_lib_process_data()`, just as seen inside the loop in example1's `main()`.

    (While a harness doesn't need to exactly imitate the application's usage of libraries, there are a variety of issues you can run into when straying too far. In this case, blindly trying to fuzz `my_custom_c_lib_process_data()` alone will cause the library to issue a "bad format!" error, whereas the combination of `MyCustomCxxLib::process_data()`-then-`my_custom_c_lib_process_data()` will work fine. This particular case is somewhat artificial, but stereotypical of real-world harnessing efforts.)

3. Create function declarations that allow you to link against the shared libraries. This application didn't ship with header files, but `nm` gives you most of the information you need to recreate them!

    Directly from the `nm` output you saw before, you are able to infer
    ```
    // Return type is unknown, because C++ name mangling doesn't include return types.
    namespace MyCustomCxxLib {
        ? process_data(const char*, char*);
    }
    
    // Return type and argument types are unknown, because it's a C function.
    // In C++, C functions must be declared with extern "C".
    // This lets C++ know to look for the unmangled name when linking.
    extern "C" ? my_custom_c_lib_process_data(???);
    ```

    The missing types here are `int`, `void`, and `char *, int`. You could determine this through trial and error, or via reverse engineering.

4. See `harness.cxx`; or, if you think you know what to do, try writing one on your own first. Ensure that you can compile, run, and fuzz this harness before moving on.

Warning: this strategy works best when using the same C++ compiler and platform as the target libraries were built with. For example, things may not work if you attempt to compile your harness with g++ when the library was compiled with clang++. In particular: g++'s libstdc++ changed its implementation of std::string a few years ago, so older (still in use!) versions of g++ toolchains are not binary compatible with recent versions. (Particularly for g++, solving this is sometimes as easy as switching between `-D_GLIBCXX_USE_CXX11_ABI=0` and `-D_GLIBCXX_USE_CXX11_ABI=1`.)

### Example 2: C++ Objects

TODO: Example where the harness needs to replicate C++ classes and call C++ constructors.

### Exercise 1: TODO

### Exercise 2: Mapnik test code.

TODO: (I haven't totally settled on the mapnik example, still deciding)

This exercise is much more of a "real" application than previous examples and exercises. The code is modified test code from [https://github.com/mapnik/mapnik](https://github.com/mapnik/mapnik), but treat all mapnik library code as if the source were unavailable for the purposes of this exercise. (Feel free to consult the source of any more standard open source libraries used in this exercise, e.g. boost or gui/rendering libraries.)

Your goal is 

### Conclusion

TODO

### Addendum

Harnessing is an ad-hoc process, and your experience will rarely conform exactly to the above examples. Get creative! Here are some tricks I've used before:

* Combine this strategy with LD_PRELOAD to mock out functions "below" the functions used by your harness.

* For C harnesses, use the Hex-Rays decompiler to automatically generate a header file for you (but be prepared to fix it up, IDA rarely gets everything exactly right).

* A C++ library can be linked to by a C (or even assembly) harness, if the C harness calls the mangled names (and, for some platforms, uses compiler extensions to declare alternate calling conventions). This can work around many issues with C++ linking, foreign STLs, etc.

* In fact, shared libraries written in almost any language can be treated as if they were written in C. A C harness can load and interact with them, although you'll probably also need to load and initialize that language's runtime libraries first.

* If the shared library doesn't seem to work correctly because the application initializes it a way that you can't replicate, try moving your harness "main()" into some function in an LD_PRELOAD object. By launching the original application executable with this harness-LD_PRELOAD, you can cause your harness to run after the application has performed initialization.
