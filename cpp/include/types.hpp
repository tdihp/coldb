#ifndef INCLUDED_COLDB_TYPES_HPP
#define INCLUDED_COLDB_TYPES_HPP
namespace coldb{
// storage data types
typedef signed char I8;
typedef unsigned char U8;
typedef signed short I16;
typedef unsigned short U16;
typedef signed int I32;
typedef unsigned int U32;

// in-program data types
typedef unsigned short COLPT;
typedef unsigned int PKGPT;
typedef char* DATA_PTR;

typedef enum E_COMPRESS
{
  PLAIN = 0,
  RUN0 = 1,
  RUN1 = 2,
  ENUM = 3,
} E_COMPRESS;

}
#endif

