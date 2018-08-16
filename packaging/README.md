## Mayhem Package Lab 
This lab will cover some more packaging configuration options such as
environment variables and where to store configuration files. The lab will
have exercises for the user to practice their knowledge on several targets.

### Background
Mayhem packaging is a critical step in ensuring a binary will perform analysis
effectively. The package will provide Mayhem everything the analysis engine 
needs to successfully execute the binary to include all the dependencies, any
configuration files and specifying how exactly to run the binary. 

### Requirements
* Experience with the Mayhem Client and UI
* Basic knowledge of Mayhem package to package simple targets 

### Environment Variables
Sometimes, a binary requires an enviornment variable to either execute
successfully or to reach a meaningful section of code. To set an 
environment variable, simply populate the `env:` parameter in the config file.

Below is an example
```
{
    "fuzzers": [
        {
            "env" : {"ENV_VAR" : "value"},
            "library_path": "root/usr/lib/x86_64-linux-gnu:root/lib/x86_64-linux-gnu",
            "target_args": [
                "-d",
                "root/etc/apache",
                "-f",
                "httpd.conf",
                "-e",
                "info",
                "-DFOREGROUND"
            ],
            "target": "root/usr/sbin/apache2",
            "network":
            {
                "url": "tcp://localhost:8080",
                "is_client": false
            }
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

### Exercise 2: Package Relay
Run through as many of the following targets to see if you can effectively
package and run the targets to achieve reasonable code coverage. 

### Conclusion
Proper packaging of a target is the crux of ensuring Mayhem will know how to 
properly execute the target under test. Binaries may have several requirements
in order to reach interesting code and this provides options to set some
configuration settings in order to achieve this. Anything outside of this 
will require more advanced techniques that will be covered in other labs. 
