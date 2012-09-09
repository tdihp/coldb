# ColdB

ColdB is a column-oriented static database-like storage framework

## What is it?

ColdB consists:
* a table schema reader (Python)
* a data-generator (Python)
* a code-generator (generates C++ code)

Aiming at small-amount of data
(16-bit equalivent data-pointer,larger configuration will be available),
ColdB takes advantage of column-based compression techniques
to minimise storage size, and maintain performance of random-access.
Suited for mobile/embed system data storage with both
limited storage resource and CPU strength.

## How is it going?

Project just started, in heavy construction now :-D.

## License

LGPL (intended)