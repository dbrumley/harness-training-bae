

# Finding Vulnerabilities in Binary Applications

There are three main audiences who want to find vulnerabilities in binary applications.

  * Hackers, who look for vulnerabilities in binary applications, and exploit them to gain unauthorized access to computer systems.
  * Software developers, who want to test their code for correctness, bugs, and security before they ship and deliver products to customers.
  * Software consumers, who want to test applications for security vulnerabilities, discovering and mitigating those vulnerabilities before they are found by attackers.

Understanding each group, their approach, and their techniques, will allow you to pick and choose the techniques best-suited to your needs.

## Hackers

When hackers look for vulnerabilities in computer programs, they rate vulnerabilities based on a few characteristics:

  * Ease of triggering the vulnerability. Ideally, hackers want vulnerabilities which do not require complex interactions between multiple software components, or multiple, uncommon configurations to be satisfied.
  * Reliability in triggering the vulnerability. Bugs and vulnerabilities which manifest themselves once in a hundred executions are not as useful to a hacker as one which manifests every execution.
  * Vulnerabilities unpatched in the latest software, or 0-day vulnerabilities, for which no patch exists to protect victims.

Hackers do not care which software component the vulnerability is in, so long as they can trigger the vulnerability reliably.

Attackers approach fuzzing and vulnerability hunting in computer software strategically. This process is sometimes referred to as, "Targetting." There is a set of criteria hackers consider, to maximize the possibility they will quickly find vulnerabilities in computer programs.

  - Hackers will read changelogs and release notes for software. New features are less tested, and more likely to contain flaws, than software which has existed and been maintained for years.
  - In addition to testing an entire program, hackers will break a program into individual components and test those individually. If a program parses binary files, for examples, hackers may fuzz just the binary file parser, separate from the rest of the program.
  - Hackers will spend a great deal of time understanding what the format of input to the 

## Software Consumers

Software consumers often find themselves in a hard place. 