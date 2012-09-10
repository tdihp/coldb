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

## Limited support of backward compatibility

Due to it's metaprogramming nature, It is easy to generate a connection
interface for former schema, as long as the new-schema do NOT make these
changes:
* add new table
* change datatype of a column
* change pkey/skey

And anything else are compatible:
* remove a column
* add a default-able column
* delete tables

## How is it going?

Project just started, in heavy construction now :-D.

## License

LGPL (intended)
