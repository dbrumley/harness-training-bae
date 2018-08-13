## Network Binary Lab
In this lab, we will package a network binary for analysis through
Mayhem. This will also cover more in depth the configuration
options for Mayhem. 

### Background
This is an introductory lab to teach students how Mayhem accepts
binaries listening on a network socket easily and without harnessing.

TODO: put packaged bacnet harness in solutions directory. only have bacnet 
binary in root. 

### Requirements
* Mayhem
* Your favorite editor

### Mayhem Configuration
Explain each network option for the config
Explain that any file (such as a config file) to be uploaded must go in root/
Explain the corpus directory

### Example 1: Bacnet
TODO: explain bacnet

  1. First we have to understand the target at test so we will run the binary
  to see what options it will need to run in an meaningful manner. 
  TODO: fill in with instructions to run and identify/explain flag options. 
  Show it is running successfully. 
  2. Second we run `mayhem package` to pull all the dependencies for the binary
  and create a default Mayhem configuration file. 
    
    mayhem package bacnet

  3. TODO: explain how to edit config
  4. Upload and run for short analysis
    mayhem upload bacnet_target/ --start-sword --duration 30
  5. Add seed to reproduce crash

### Exercise 2: Lighttpd
The student will apply their knowledge to fuzz lighttpd. 

### Conclusion
This lesson went into the details of the Mayhem configuration file and showed
how to package network binaries. 

