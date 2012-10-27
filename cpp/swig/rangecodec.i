%module rangecodec
%include "std_string.i"
%{
#define SWIG_FILE_WITH_INIT
#include "coldb/types.hpp"
#include "coldb/rangecodec.hpp"
using namespace coldb;

%}

%inline %{
#include <stdio.h>
#include <string>
class StrStream
{
public:
  StrStream(std::string str) : str_(str), i_(0){}
  ~StrStream() {}
  void put(char chr)
  {
    str_.push_back(chr);
  }
  int get() {return str_[i_++];}
  std::string getStr() {return str_;}
  U32 getI() {return i_;}
private:
  U32 i_;
  std::string str_;
};
%}

%include "coldb/types.hpp"
%include "coldb/rangecodec.hpp"
using namespace coldb;


%template(RangeCore) RangeCore<10, StrStream, unsigned long long>;

