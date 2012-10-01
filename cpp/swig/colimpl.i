%module colimpl
%include "std_string.i"
%{
#define SWIG_FILE_WITH_INIT
#include "coldb/types.hpp"
#include "coldb/column.hpp"
using namespace coldb;
%}

%include "coldb/column.hpp"

%template(Plain_b) coldb::PlainImpl<coldb::I8>;
%template(Plain_B) coldb::PlainImpl<coldb::U8>;
%template(Plain_h) coldb::PlainImpl<coldb::I16>;
%template(Plain_H) coldb::PlainImpl<coldb::U16>;
%template(Plain_i) coldb::PlainImpl<coldb::I32>;
%template(Plain_I) coldb::PlainImpl<coldb::U32>;

%template(Run0_b) coldb::Run0Impl<coldb::I8, coldb::U16>;
%template(Run0_B) coldb::Run0Impl<coldb::U8, coldb::U16>;
%template(Run0_h) coldb::Run0Impl<coldb::I16, coldb::U16>;
%template(Run0_H) coldb::Run0Impl<coldb::U16, coldb::U16>;
%template(Run0_i) coldb::Run0Impl<coldb::I32, coldb::U16>;
%template(Run0_I) coldb::Run0Impl<coldb::U32, coldb::U16>;

%template(Run1_b) coldb::Run1Impl<coldb::I8, coldb::U16>;
%template(Run1_B) coldb::Run1Impl<coldb::U8, coldb::U16>;
%template(Run1_h) coldb::Run1Impl<coldb::I16, coldb::U16>;
%template(Run1_H) coldb::Run1Impl<coldb::U16, coldb::U16>;
%template(Run1_i) coldb::Run1Impl<coldb::I32, coldb::U16>;
%template(Run1_I) coldb::Run1Impl<coldb::U32, coldb::U16>;

%template(Enum_h) coldb::Run1Impl<coldb::I16, coldb::U8>;
%template(Enum_H) coldb::Run1Impl<coldb::U16, coldb::U8>;
%template(Enum_i) coldb::Run1Impl<coldb::I32, coldb::U8>;
%template(Enum_I) coldb::Run1Impl<coldb::U32, coldb::U8>;

%template(Struct_7) coldb::StructImpl<7>;
%template(Struct_8) coldb::StructImpl<8>;

%template(Blob_1) coldb::BlobImpl<coldb::U16, 1>;
%template(Blob_2) coldb::BlobImpl<coldb::U16, 2>;
%template(Blob_4) coldb::BlobImpl<coldb::U16, 4>;

