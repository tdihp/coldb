# ColdB

ColdB is a column-oriented static database-like storage framework

## What is it?

ColdB consists:
* a table schema reader (Python)
* a data-generator (Python)
* a code-generator (generates C++ client API code)
* a C++ column access library

Aiming at small-amount of data(up to 2GB per column),
ColdB takes advantage of column-based compression techniques
to minimise storage size, while maintain performance of random-access
and sorted search (O(log n) at most).

Currently, following compression techniques have been used:
* type trapping (for array short[0,1,2,3], store char[0,1,2,3] instead)
* Run-length encoding variations
* Dictionary encoding
* Frame of reference encoding

Suited for mobile/embed system data storage with both
limited storage resource and CPU strength.

## Limited support of backward compatibility (not available yet)

Due to the metaprogramming nature of Client API, It is easy to
generate a connection interface for former schema,
as long as the new-schema do NOT make these changes:
* change datatype of a column
* change pkey/skey of a table

And anything else are compatible:
* add new table
* remove a column
* add a default-able column
* delete tables

## How is it going?

Project just started, in heavy construction now :-D.

## License

BSD 2-Clause, see the LICENSE file for details.
