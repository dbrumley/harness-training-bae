## Mayhem-profile Lab
## Alexander Taylor & Michal
--------------------------------------------------------------------------------
## Internal - Remove from document  before the tutorial:
TODO:
Mayhem-profile needs to be installed on the provided VMs.
Either Ubuntu/Debian with mayhem-profile installed.
Run:  sudo echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid  
Create a profie-openssl-lab with the test cases & two libraries version (available at the mayhem-profile repo).

Known issues, need to be fixed for the LAB
https://forallsecure.atlassian.net/browse/K8-466 
1. valgrind needs to be added as a dependency for `pip` installs of triager
2. @@ need to add a warning when we’re not getting CPU clocks/cycles back from `perf` to explain why (also should look into this more to get a better explanation) 
3. Profile ignores output file?

----------------------------------------------------------------------------------------------

### Background

Mayhem profile is a tool for comparing two or more targets across given
test cases.
It can be used for both performance and regression testing.
Mayhem profile works on a suite of test cases. This suite can be a partial or full set of Mayhem generated test cases.
The user will downloaded test suites from Mayhem, and will point Mayhem-profile to the location of the tests and the targets that should be compared.
Mayhem profile will run the targets on all the test cases in the input directory, and will output performance metrics and crash status for each test case.
More specifcally, Mayhem profile can help testing the following:

1. A newer version of the target fixed an issue that was detected by mayhem (run "crash" test cases)
2. A newer version of the target didn't introduce performance regeressions. (run "non-crash" test cases)
3. A newer version didn't introduce new bugs (run all test cases)

In the lab, we will see an example of using Mayhem profile as a standalone CLI tool, but it can be integrated into a CI/CD pipeline in the future.

### Requirements

* mayhem-profile needs to be istalled on the machine:
To validate that it is installed correctly

``` $ mayhem-profile
 usage: mayhem-profile [-h] [-t TIMEOUT] [-i ITERATIONS] [-v]
       input output harnesses [harnesses ...]
 mayhem-profile: error: the following arguments are required: input, output,   harnesses.
```

### Exercise: Profiling two versions of openssl

While running Mayhem on a known open source library (OpenSSL), Mayhem detected a crash!
(This crash is a CVE found by Mayhem, more information here: [OpenSSL CVE](https://github.com/openssl/openssl/commit/610b66267e41a32805ab54cbc580c5a6d5826cb4#diff-5e137ee8834b94e9cb3fde78d900a21cL233))
A new version of OpenSSL was released, and we want to test if the bug was fixed and make sure that the library performance was not hit because of the fixed.

In this exercise, we will use a pre-downloaded set of mayhem generated test cases, to test that the bug was fixed, and look for performance issues.

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

| input     |  metric   | openssl-1.0.1b |  openssl-1.0.1u |
| :-------: | :-------: | :-------------:| :-------------: |
| test-578 | crashed   |   True         |  False          |
| test-578 | cycles    |                |  6185745        |
| test-578 | timed out | False          |  False          |
| test-578 | cpu-clock |                |  1.799397       |
| test-577 | crashed   | True           |  False          |
| test-577 |  cycles   |                |  6528123        |
| test-577 | timed out | False          |  False          |
| test-577 | cpu-clock |                |  1.927653       |
| test-579 | crashed   | True           |  False          |
| test-579 | cycles    |                |  6146520        |
| test-579 | timed out | False          |  False          |
| test-579 | cpu-clock |                |  1.801818       |
| test-576 | crashed   | True           |  False          |
| test-576 | cycles    |                |  6462542        |
| test-576 | timed out | False          |  False          |
| test-576 | cpu-clock |                |  1.898554       |
| test-581 | crashed   | True           |  False          |
| test-581 | cycles    |                |  6241992        |
| test-581 | timed out | False          |  False          |
| test-581 | cpu-clock |                |  1.831641       |
| test-575 | crashed   | True           |  False          |
| test-575 | cycles    |                |  6268562        |
| test-575 | timed out | False          |  False          |
| test-575 | cpu-clock |                |  1.864625       |
| test-582 | crashed   | True           |  False          |
| test-582 | cycles    |                |  6229571        |
| test-582 | timed out | False          |  False          |
| test-582 | cpu-clock |                |  1.769081       |
| test-580 |  crashed  |  True          |  False          |
| test-580 |  cycles   |                |  6367691        |
| test-580 | timed out | False          |  False          |
| test-580 | cpu-clock |                |  1.871983       |

It is easy to see that the new version does not crash with any of the test cases that caused a crash in the first version.
However, we only downloaded the set of crashing test cases.

#### Download all the test cases

Using Mayhem client, upload the first target to Mayhem, download all the test cases, and compare performance for non crashing test cases.
Also, verify that the new version doesn't crash with any of the test cases that were downloaded (package might be a bit different from the one included).

#### Use the packgaed version of openssl-1.0.1b which is avaliavle at

``` $ <path_to>/mayhem-profile/lab-2
```
Upload to mayhem, and run mayhem:
```
$ mayhem upload -u <your_mayhem_url> openssl-cms-test/ --start-sword --duration 1200
```

Download new test cases using mayhem client:
```
$ mayhem testsuite -u <your_mayhem_url> download <job_id>
```

Run mayhem profile with both "crashing" and "non crashing" test cases.
(some additional sample test cases are attched in mayhem-profile/lab-2/more-testcases)
Look for performance regressions/new bugs in the new version (reminder, the new version is mayhem-profile/lab-1/openssl-1.0.1u)
