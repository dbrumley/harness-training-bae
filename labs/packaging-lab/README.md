## Mayhem Package Lab 
This lab will cover some more packaging configuration options such as
environment variables and where to store configuration files. 

### Background
Mayhem packaging is a critical step in ensuring a binary will perform analysis
effectively. The package will provide Mayhem everything the analysis engine 
needs to successfully execute the binary to include all the dependencies, any
configuration files and specifying how exactly to run the binary. 

### Requirements
* Experience with the Mayhem Client and UI
* Basic knowledge of Mayhem package to package simple targets 

### Paths
When programs run and reference other files, they need to describe the
locations of other files with paths. When packages are uploaded, it is
important to be aware of paths and locations to make sure that programs
will be able to find their dependencies when run with Mayhem.

When launched, programs are isolated in a process jail, which gives
each program its own view of the file system. By default, Mayhem will
launch the program by running in the directory `/`. The files from
the package's `root` folder will be mounted in the jail at `/root`.

In general, if one needs to reference paths inside the root folder,
they can therefore use either `/root/path/to/target` or `root/path/to/target`.

### Jail Environment
In addition, when a program launches inside the jail, the user and group
are fixed to `fas`. This is useful to note for some programs which require
knowing which user they run as, such as server applications.

As many programs write to temporary files, the jail allows programs to
write to files in `/tmp/`, `/var/tmp/`, and `/dev/shm/`. These can be used
for scratch space for things like PID lock files or other small files that
a target will create.

### Environment Variables
Sometimes, a binary requires an enviornment variable to either execute
successfully or to reach a meaningful section of code. To set an 
environment variable, simply populate the `env:` parameter in the config file.

Below is an example
```
{
    "fuzzers": [
        {
            "env" : {"ENV_VAR1" : "value", "ENV_VAR2" : "value2"},
            "library_path": "root/usr/lib/x86_64-linux-gnu:root/lib/x86_64-linux-gnu",
            "target_args": [
                "@@"
            ],
            "target": "root/bin/example",
        }
    ]
}
```

### Exercise 1: Package a complex target (ex_app)
This target will have several requirements in order to execute succesfully. 
The user must figure out how to set environment variables and place 
configuration files to allow effective analysis of the target. 

Navigate to the ex_app directory. Look through the source
to figure out how the binary runs and what settings need to be configured in 
order to reach the interesting, buggy sections of code. 

Package the binary and upload to see if the analysis runs successfully to find
the bugs.

If the package uploads successfully but the analysis does not seem to be 
achieving much coverage, view the testcase details to see the stdout and 
figure out what the target is looking for and what is missing from the package

### Conclusion
Proper packaging of a target is the crux of ensuring Mayhem will know how to 
properly execute the target under test. Binaries may have several requirements
in order to reach interesting code and this provides options to set some
configuration settings in order to achieve this. Anything outside of this 
will require more advanced techniques that will be covered in other labs. 
