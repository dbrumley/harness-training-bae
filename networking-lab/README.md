## Network Binary Lab
In this lab, we will package a network binary for analysis through
Mayhem. This will also cover more in depth the configuration
options for Mayhem.

### Background
This is an introductory lab to teach students how Mayhem accepts
binaries listening on a network socket easily and without harnessing.

### Requirements
* Mayhem
* Your favorite editor

### Mayhem Configuration
The SMART config for networked targets requires specific fields to be
populatated.  The fields are as follows:

* URL: This contains the protocol the target uses (udp or tcp), the ip
address of the target (localhost), and the port the target listens/connects
on.  It has the form: `<protocol>://localhost:<port>`
* is_client: True or False dependening on whether or not the target is
a client
* timeout: Timeout in ms of how long to wait before closing the network
connection

Here is an example config:
```
{
    "fuzzers": [
        {
            "target": "root/myserver",
            "target_args": [],
            "network": {
                "url": "udp://localhost:124",
                "is_client": false,
                "timeout" : 2000
            }
        }
    ]
}
```

### Example: Bacsrv
At FAS we operate on the binary level, and know nothing about the target
For the purposes of this lab, we assume the student also knows nothing
about the target.

Our target is Bacsrv.  Below is a step by step process for how to analyze
the binary:

1.  Get context by googling the target.  We see Bacnet is a data
communication protocol for building automation control and
networks.  Bacsrv implements this protocol.

2. Run `mayhem package` to pull all the dependencies for the binary
  and create a default Mayhem configuration file.

3. Edit the network config.  Follow the below steps to figure out
the correct information:\s\s
    a. Run the target to see if it provides anything useful.
```
$ ./bacserv
BACnet Server Demo
BACnet Stack Version 0.9.1
BACnet Device ID: 260001
Max APDU: 1476
```
Unfortunately, the above output doesn't tell us anything.

    b.  Run strace to identify the port and protocol.
```
strace -f -o /tmp/slog ./bacsrv
```
`-f` indicates follow children, and `-o` is the file our results are written to.

    c.  Because this is a server, we know it binds to a port.  Grep for bind in the results:
```
$ grep bind /tmp/slog
20399 bind(3, {sa_family=AF_INET, sin_port=htons(47808), sin_addr=inet_addr("0.0.0.0")}, 16) = 0
```
We see that the target is IPV4 (AF_INET) and bound to port 47808.

    d.  To identify the protocol, grep for `socket`.
```
$ grep socket /tmp/slog
20399 socket(PF_INET, SOCK_DGRAM, IPPROTO_IP) = 3
20399 socket(PF_INET, SOCK_DGRAM, IPPROTO_IP) = 3
20399 socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP) = 3
```
We see this uses UDP.

4.  The package is ready, to begin fuzzing run:
`mayhem upload bacnet/ --start-sword --duration 30`

### Tips
* Run the help menu to see what capabilities are available.  Always look
for the option to run the target in the foreground (ie don't daemonize).
* Strace can be used to identify missing configuration files or modules.
* A good starting corpus is very important.  A good place to start is by
capturing real network requests.

### Exercise: Lighttpd
The student will apply their knowledge to fuzz lighttpd.

### Conclusion
This lesson went into the details of the Mayhem configuration file and showed
how to package network binaries.

