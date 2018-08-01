 # Packaging and analyzing simple binary executables.

This tutorial is designed to be the first in a series of tutorials on how to use MAYHEM to work with binary applications. In this tutorial, we will:

  * Package a simple binary executable for analysis with MAYHEM.
  * Upload the package to MAYHEM for analysis.

## MAYHEM: A high-level overview

MAYHEM discovers inputs which explore different locations in an application. Similar to how developers write unit tests to cover different lines of source code, MAYHEM generates program inputs that cover different blocks of assembly code. This concept is called, "Coverage-based fuzzing," which is a type of dynamic analysis.

We need two basic components for coverage-based fuzzing: a way to intelligently generate program inputs, and a way to measure the program while it is running.

### Mutation-Based Input Generation and Symbolic Execution

MAYHEM uses two main methods to disocver new program inputs, mutation-based input generation and symbolic execution.

Mutation-based input generation starts with a corpus of inputs for a program, and then makes alterations, or mutations, to those inputs. Assume, for example, we have a program which receives HTTP requests. If we start our analysis with a valid HTTP request, small changes to that HTTP request will cause our program to execute new code paths, without the work of attempting to discover what a valid HTTP request looks like in the first place.

Second, MAYHEM uses symbolic execution to generate new program inputs. If our program is deterministic, then there is a direct mapping between an input to the program, and the path the program takes. Symbolic Execution creates a model of this path, converting a series of instructions executed into a system of equations where the free variables are inputs to our program, and we are solving for conditional branches to explore new paths through the program. These equations are passed to SAT/SMT solvers, which specialize in quickly solving these formula. The result are new program inputs which will explore new paths through the program.

### Measuring a Program

MAYHEM uses a variety of methods to measure programs. MAYHEM can use compile-time instrumentation for libfuzzer or afl, two popular coverage-based fuzzing utilities, to track assembly code block coverage. AFL can also use dynamic binary instrumentation to track coverage statistics.

MAYHEM makes use of debugger APIs in supported operating systems to determine when invalid conditions are met, such as reads and writes to invalid addresses, or when execution flow has deviated to incorrect areas of memory.

Finally, MAYHEM runs common memory checking tools to check for problems such as reads beyond the bounds of a heap allocation that do not necessarily trigger errors which would be caught by a debugger.

## Requirements for our binary

In order for our binary to be analyzed with MAYHEM, the following properties must hold:

  * The binary application must accept input through a means supported by MAYHEM.
  * The binary application must run on an architecture and operating system supported by MAYHEM.
  * You are looking for errors in the binary you are testing. For example, if you ran the python interpreter over python scripts, MAYHEM will not find errors in the python scripts, MAYHEM will find errors in the python interpreter.

## Packaging `objdump`

`objdump` is an application distributed with GNU binutils to dump and display information about programs stored in common binary executable file formats. We will package `objdump` for MAYHEM, and upload `objdump` to our instance of MAYHEM Sword.

To begin, we will install `objdump`. To do this on a debian-based distro (Debian, Ubuntu, etc.), we run:

    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y binutils

We can now run `objdump` against a binary of our choosing.

```
root@d5ec5618a4ed:~# objdump /bin/ls
Usage: objdump <option(s)> <file(s)>
 Display information from object <file(s)>.
 At least one of the following switches must be given:
  -a, --archive-headers    Display archive header information
  -f, --file-headers       Display the contents of the overall file header
  -p, --private-headers    Display object format specific file header contents
  -P, --private=OPT,OPT... Display object format specific contents
  -h, --[section-]headers  Display the contents of the section headers
  -x, --all-headers        Display the contents of all headers
  -d, --disassemble        Display assembler contents of executable sections
  -D, --disassemble-all    Display assembler contents of all sections
  -S, --source             Intermix source code with disassembly
  -s, --full-contents      Display the full contents of all sections requested
  -g, --debugging          Display debug information in object file
  -e, --debugging-tags     Display debug information using ctags style
  -G, --stabs              Display (in raw form) any STABS info in the file
  -W[lLiaprmfFsoRt] or
  --dwarf[=rawline,=decodedline,=info,=abbrev,=pubnames,=aranges,=macro,=frames,
          =frames-interp,=str,=loc,=Ranges,=pubtypes,
          =gdb_index,=trace_info,=trace_abbrev,=trace_aranges,
          =addr,=cu_index]
                           Display DWARF info in the file
  -t, --syms               Display the contents of the symbol table(s)
  -T, --dynamic-syms       Display the contents of the dynamic symbol table
  -r, --reloc              Display the relocation entries in the file
  -R, --dynamic-reloc      Display the dynamic relocation entries in the file
  @<file>                  Read options from <file>
  -v, --version            Display this program's version number
  -i, --info               List object formats and architectures supported
  -H, --help               Display this information
root@d5ec5618a4ed:~# 
```

Running with no flags isn't very helpful. If we take a look at the help menu that's printed out, we see there's a variety of flags printed out. The flags `-x` and `-s` look useful. Let's try running again with those flags.

```
root@d5ec5618a4ed:~# objdump -xD /bin/ls | head

/bin/ls:     file format elf64-x86-64
/bin/ls
architecture: i386:x86-64, flags 0x00000150:
HAS_SYMS, DYNAMIC, D_PAGED
start address 0x0000000000005430

Program Header:
    PHDR off    0x0000000000000040 vaddr 0x0000000000000040 paddr 0x0000000000000040 align 2**3
         filesz 0x00000000000001f8 memsz 0x00000000000001f8 flags r-x
         
...
         
  1a:   66 61                   data16 (bad) 
  1c:   61                      (bad)  
  1d:   35 62 64 31 30          xor    $0x30316462,%eax
  22:   65 63 63 64             movslq %gs:0x64(%rbx),%esp
  26:   2e 64 65 62             cs fs gs (bad) {%k6}
  2a:   75 67                   jne    93 <_init@@Base-0x3435>
  2c:   00 00                   add    %al,(%rax)
  2e:   00 00                   add    %al,(%rax)
  30:   c2 01 46                retq   $0x4601
  33:   f8                      clc    
root@d5ec5618a4ed:~# 
```

Terrific. Now we know exactly how we want to invoke `objdump`, with the `-xD` flags.

To package this binary, we run `mayhem package /usr/bin/objdump`. Let's try that out now.

```
root@d5ec5618a4ed:~# mayhem package /usr/bin/objdump
INFO:root:Packaging application: /usr/bin/objdump
INFO:root:Packaging dependency: /usr/bin/objdump -> /tmp/objdump-wng7lsdf/root/usr/bin/objdump
INFO:root:Packaging dependency: /lib/x86_64-linux-gnu/libz.so.1 -> /tmp/objdump-wng7lsdf/root/lib/x86_64-linux-gnu/libz.so.1
INFO:root:Packaging dependency: /usr/lib/x86_64-linux-gnu/libopcodes-2.28-system.so -> /tmp/objdump-wng7lsdf/root/usr/lib/x86_64-linux-gnu/libopcodes-2.28-system.so
INFO:root:Packaging dependency: /usr/lib/x86_64-linux-gnu/libbfd-2.28-system.so -> /tmp/objdump-wng7lsdf/root/usr/lib/x86_64-linux-gnu/libbfd-2.28-system.so
INFO:root:Generating default configuration under: /tmp/objdump-wng7lsdf/config.json
INFO:root:Packaged /usr/bin/objdump under: /tmp/objdump-wng7lsdf
root@d5ec5618a4ed:~# 
```

There are a few files and folders inside the package we have created at `/tmp/objdump-wng7lsdf`.

```
root@d5ec5618a4ed:~# ls -lh /tmp/objdump-wng7lsdf
total 12K
-rw-r--r-- 1 root root  277 Jul  9 20:45 config.json
drwxr-xr-x 2 root root 4.0K Jul  9 20:45 corpus
drwxr-xr-x 4 root root 4.0K Jul  9 20:45 root
```

The `config.json` file contains auto-populated configuration information for MAYHEM, informing MAYHEM how to invoke and run our binary under test.

The `corpus` directory contains seed inputs. Earlier, when we talked about mutation-based input generation, these are the inputs that MAYHEM would mutate. We won't add any seed inputs to the `corpus` directory for this example, and allow MAYHEM to discover inputs from scratch.

The root directory contains all of the files and dependencies required for MAYHEM to invoke and run the binary we wish to test. This directory has been auto-populated with the dynamically-linked runtime dependencies for us.

We do need to modify the `config.json` file. Let's take a look at what's inside first.

```
root@d5ec5618a4ed:~# cat /tmp/objdump-wng7lsdf/config.json 
{
    "fuzzers": [
        {
            "target_args": [
                "@@"
            ],
            "target_input": "@@",
            "library_path": "root/usr/lib/x86_64-linux-gnu:root/lib/x86_64-linux-gnu",
            "target": "root/usr/bin/objdump"
        }
    ]
}
```

For the purposes of this tutorial, we are only concerned with the `"target_args"` field. This is a json array of command-line arguments to be passed to the target binary. `"@@"` is a special argument that tells MAYHEM, "Create an input filename for me, and place it here." We want to pass the command line argument `-xD` before `@@`, so we will change `"target_args"` to look like this:

```
            "target_args": [
                "-xD",
                ""@@"
            ]
```

We're now going to upload this package to MAYHEM. We need the URL for the running instance of MAYHEM we wish to upload this package to. For me, this URL is `http://192.168.99.101:32434`.

To upload, I will type:

    mayhem upload --start-sword -u http://192.168.99.101:32434/ /tmp/objdump-wng7lsdf

`--start-sword` tells MAYHEM to start fuzzing as soon as the binary is uploaded, and `-u` allows us to specify a URL to our specific instance of MAYHEM.

We can now browse to http://192.168.99.101:32434, or whatever your specific url is, and watch MAYHEM starting to analyze our binary.

![Watching MAYHEM analyze our binary](images/mayhem-gui-screenshot.png)