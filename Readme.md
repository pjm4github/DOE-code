# Origin Landing Page

Look here **[GridAPPS-D](https://gridapps-d.org/about)** for the original source code that is the basis for this repo.

There's also an (obsolete) [wiki page](http://gridlab-d.shoutwiki.com/wiki/Main_Page) ...

...and a [4-day course](https://sourceforge.net/p/gridlab-d/code/HEAD/tree/course/FourDayCourse/) which has been copied to the *./Training* directory.

## About this code

This repository is a refactor of the GridAPPS-D application and supporting services.
It is both an experiment and a learning effort to see what is in the DOE released software project and how much can be 
reused for the purpose of utility operations. 

The python code entry point is here:

    TBD

This is the location of the starting point for understanding GridLAB-D


The run time logic appears to be c code. 
Explanation of the [runtime](%USERPROFILE%\Documents\GitHubGit\GitHub\gridlab-d-5.2\gldcore\gridlabd.h).

The [main event loop](%USERPROFILE%\Documents\GitHubGit\GitHub\gridlab-d-5.2\gldcore\exec.cpp)


Note that the CIM standard library as referenced has been converted and is available 
in [TC57CIM](https://github.com/pjm4github/TC57CIM). This is the library that CIMHub will reference to 
validate the functional SIM model. 

###  Derivative Works
There are derivative code bases that are of interest:

* [gridspice](https://code.google.com/archive/p/gridspice/source)

  * [Smart Grid](https://isl.stanford.edu/~abbas/papers/GridSpice%20A%20Distributed%20Simulation%20Platform%20for%20the%20Smart%20Grid.pdf)

  * [Paper](https://www.semanticscholar.org/paper/GridSpice%3A-A-Distributed-Simulation-Platform-for-Anderson-Du/aa3799717576f58fc6b10389d71c3a2894be42f7)
