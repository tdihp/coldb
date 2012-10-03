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

%typemap(in) void* = char*;

%template(Plain_b) PlainImpl<I8>;
%template(Plain_B) PlainImpl<U8>;
%template(Plain_h) PlainImpl<I16>;
%template(Plain_H) PlainImpl<U16>;
%template(Plain_i) PlainImpl<I32>;
%template(Plain_I) PlainImpl<U32>;

%template(Run0_b) Run0Impl<I8, U16>;
%template(Run0_B) Run0Impl<U8, U16>;
%template(Run0_h) Run0Impl<I16, U16>;
%template(Run0_H) Run0Impl<U16, U16>;
%template(Run0_i) Run0Impl<I32, U16>;
%template(Run0_I) Run0Impl<U32, U16>;

%template(Run1_b) Run1Impl<I8, U16>;
%template(Run1_B) Run1Impl<U8, U16>;
%template(Run1_h) Run1Impl<I16, U16>;
%template(Run1_H) Run1Impl<U16, U16>;
%template(Run1_i) Run1Impl<I32, U16>;
%template(Run1_I) Run1Impl<U32, U16>;

%template(Enum_h) EnumImpl<I16, U8>;
%template(Enum_H) EnumImpl<U16, U8>;
%template(Enum_i) EnumImpl<I32, U8>;
%template(Enum_I) EnumImpl<U32, U8>;

%template(Struct_7) StructImpl<7>;
%template(Struct_8) StructImpl<8>;

%template(Blob_1) BlobImpl<U16, 1>;
%template(Blob_2) BlobImpl<U16, 2>;
%template(Blob_4) BlobImpl<U16, 4>;

