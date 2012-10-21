%module colimpl
%include "std_string.i"
%{
#define SWIG_FILE_WITH_INIT
#include "coldb/types.hpp"
#include "coldb/column.hpp"
using namespace coldb;
%}
%include "coldb/types.hpp"
%include "coldb/column.hpp"
using namespace coldb;

//%typemap(in) void*& = char*;
%typemap(in) void*&
{
  $1 = (void**)(malloc(sizeof(void**)));
  *$1 = PyString_AsString($input);
}
%typemap(freearg) void*&
{
  free($1);
}
%template(Plain_b) PlainImpl<I8>;
%template(Plain_B) PlainImpl<U8>;
%template(Plain_h) PlainImpl<I16>;
%template(Plain_H) PlainImpl<U16>;
%template(Plain_i) PlainImpl<I32>;
%template(Plain_I) PlainImpl<U32>;

%template(Run0_bB) Run0Impl<I8, U8>;
%template(Run0_BB) Run0Impl<U8, U8>;
%template(Run0_hB) Run0Impl<I16, U8>;
%template(Run0_HB) Run0Impl<U16, U8>;
%template(Run0_iB) Run0Impl<I32, U8>;
%template(Run0_IB) Run0Impl<U32, U8>;

%template(Run0_bH) Run0Impl<I8, U16>;
%template(Run0_BH) Run0Impl<U8, U16>;
%template(Run0_hH) Run0Impl<I16, U16>;
%template(Run0_HH) Run0Impl<U16, U16>;
%template(Run0_iH) Run0Impl<I32, U16>;
%template(Run0_IH) Run0Impl<U32, U16>;

%template(Run0_bI) Run0Impl<I8, U32>;
%template(Run0_BI) Run0Impl<U8, U32>;
%template(Run0_hI) Run0Impl<I16, U32>;
%template(Run0_HI) Run0Impl<U16, U32>;
%template(Run0_iI) Run0Impl<I32, U32>;
%template(Run0_II) Run0Impl<U32, U32>;

%template(Run1_bB) Run1Impl<I8, U8>;
%template(Run1_BB) Run1Impl<U8, U8>;
%template(Run1_hB) Run1Impl<I16, U8>;
%template(Run1_HB) Run1Impl<U16, U8>;
%template(Run1_iB) Run1Impl<I32, U8>;
%template(Run1_IB) Run1Impl<U32, U8>;

%template(Run1_bH) Run1Impl<I8, U16>;
%template(Run1_BH) Run1Impl<U8, U16>;
%template(Run1_hH) Run1Impl<I16, U16>;
%template(Run1_HH) Run1Impl<U16, U16>;
%template(Run1_iH) Run1Impl<I32, U16>;
%template(Run1_IH) Run1Impl<U32, U16>;

%template(Run1_bI) Run1Impl<I8, U32>;
%template(Run1_BI) Run1Impl<U8, U32>;
%template(Run1_hI) Run1Impl<I16, U32>;
%template(Run1_HI) Run1Impl<U16, U32>;
%template(Run1_iI) Run1Impl<I32, U32>;
%template(Run1_II) Run1Impl<U32, U32>;

%template(Enum_h) EnumImpl<I16, U8>;
%template(Enum_H) EnumImpl<U16, U8>;
%template(Enum_i) EnumImpl<I32, U8>;
%template(Enum_I) EnumImpl<U32, U8>;

%template(Struct_7) StructImpl<7>;
%template(Struct_8) StructImpl<8>;

%template(Blob_1H) BlobImpl<U16, 1>;
%template(Blob_2H) BlobImpl<U16, 2>;
%template(Blob_4H) BlobImpl<U16, 4>;

%template(Blob_1I) BlobImpl<U32, 1>;
%template(Blob_2I) BlobImpl<U32, 2>;
%template(Blob_4I) BlobImpl<U32, 4>;

