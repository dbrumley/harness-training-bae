# Mayhem-profile Lab
(Alexander Taylor & Michal)
--------------------------------------------------------------------------------
## Internal - Remove from document  before the tutorial:
TODO:
Create container for this tutorial:
Either Ubuntu/Debian with mayhem-profile installed.
Run:  sudo echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid  
Create a profie-openssl-lab with the test cases & two libraries version (available at the mayhem-profile repo). 

Known issues, need to be fixed for the LAB 
(TODO: the list below is copied from slack chat, add Jira tasks #, once @@ opens them)
1. valgrind needs to be added as a dependency for `pip` installs of triager somehow
2. @@ need to modify the thing my `README.md` for `pip` installation in a `venv`
3. @@ need to ask SMART people if we can do relative paths (if yes, fix test…if no, make ticket for it)
4. @@ need to talk to john about the valgrind error and see if he’s aware of it - if not, file ticket and have him prioritize it higher (edited)
5. @@ need to add a warning when we’re not getting CPU clocks/cycles back from `perf` to explain why (also should look into this more to get a better explanation) 
6. Profile ignores output file?

-----------------------------------------------------------------------------------------------------------------------

Mayhem profile is a tool for comparing two or more targets across given
test cases.
It can be used for testing that a newer version of the target fixed an issue that was detected by mayhem
and also to verify that the new version doesn't introduce performance regressions.

In the lab, we will see an example of using Mayhem profile as a standalone CLI tool, but it can be integrated into a CI/CD pipeline in the future. 

## Exercise 1: Profiling two versions of openssl

While running Mayhem on a known open source library (OpenSSL), Mayhem detected a crash!
(This crash is a CVE found by Mayhem, more information here: [OpenSSL CVE](https://github.com/openssl/openssl/commit/610b66267e41a32805ab54cbc580c5a6d5826cb4#diff-5e137ee8834b94e9cb3fde78d900a21cL233))
A new version of OpenSSL was released, and we want to test if the bug was fixed and make sure that the library performance was not hit because of the fixed.

In this exercise, we will use a pre-downloaded set of mayhem generated test cases, to test that the bug was fixed, and look for performance issues.

Instructions:
Make sure that mayhem-profile is installed:

``` $ ./mayhem-profile
 usage: mayhem-profile [-h] [-t TIMEOUT] [-i ITERATIONS] [-v]
       input output harnesses [harnesses ...]
 mayhem-profile: error: the following arguments are required: input, output,   harnesses.
```

Run mayhem-profile:

```$cd mayhem-profile/lab-1 && ls
```

This directory contains the following :
Two versions of openssl:
Openssl-1.0.1u - the original library that contains the bug.
Openssl-1.0.1b - the updated library with the bug fix.
test-cases : test cases that caused the crash that were downloaded from Mayhem.  
	
```
$ cd profile-openssl-lab
#create an output file:
$ touch profile.output
#run mayhem-profile
$ ./mayhem-profile /test-cases profile.output openssl-1.0.1u openssl-1.0.1b
```

Examine the results:
input     metric     openssl-1.0.1b    openssl-1.0.1u
--------  ---------  ----------------  ----------------
test-578  crashed    True              False
test-578  cycles                       6185745
test-578  timed out  False             False
test-578  cpu-clock                    1.799397
test-577  crashed    True              False
test-577  cycles                       6528123
test-577  timed out  False             False
test-577  cpu-clock                    1.927653
test-579  crashed    True              False
test-579  cycles                       6146520
test-579  timed out  False             False
test-579  cpu-clock                    1.801818
test-576  crashed    True              False
test-576  cycles                       6462542
test-576  timed out  False             False
test-576  cpu-clock                    1.898554
test-581  crashed    True              False
test-581  cycles                       6241992
test-581  timed out  False             False
test-581  cpu-clock                    1.831641
test-575  crashed    True              False
test-575  cycles                       6268562
test-575  timed out  False             False
test-575  cpu-clock                    1.864625
test-582  crashed    True              False
test-582  cycles                       6229571
test-582  timed out  False             False
test-582  cpu-clock                    1.769081
test-580  crashed    True              False
test-580  cycles                       6367691
test-580  timed out  False             False
test-580  cpu-clock                    1.871983

It is easy to see that the new version does not crash with any of the test cases that caused a crash in the first version.
However, we only downloaded the set of crashing test cases.

### Download all the test cases

Using Mayhem client, upload the first target to Mayhem, download all the test cases, and compare performance for non crashing test cases.
Also, verify that the new version doesn't crash with any of the test cases that were downloaded (package might be a bit different from the one included).

#### You can use the packgaed version of openssl-1.0.1b which is avaliavle at

``` $ ./mayhem-profile/lab-2
```

TODO: Make the print screen prettier? (colors , etc.. )


