#ifndef INCLUDED_COLDB_FACTORY_HPP
#define INCLUDED_COLDB_FACTORY_HPP

#include <string>
#include <climits>
#include "coldb/types.hpp"
#include "coldb/column.hpp"

namespace coldb
{

template <template<typename IFType> class IF,
          template<typename IFType, class Impl> class IFImpl,
          typename IFType,
          typename PT,
          typename ET,
          typename DT>
IF<IFType>* _i_col_factory_l2(U32 compress_id,
                              void*& data_ptr,
                              I32 data_size)
{
  switch (compress_id)
  {
    case PLAIN:
      return new IFImpl<IFType, PlainImpl<DT> >(data_ptr, data_size);
    case RUN0:
      return new IFImpl<IFType, Run0Impl<DT, PT> >(data_ptr, data_size);
    case RUN1:
      return new IFImpl<IFType, Run1Impl<DT, PT> >(data_ptr, data_size);
    case ENUM:
      return new IFImpl<IFType, EnumImpl<DT, ET> >(data_ptr, data_size);
    default:
      return 0;  // TODO: exception throw
  }
}

template <template<typename IFType> class IF,
          template<typename IFType, class Impl> class IFImpl,
          typename IFType,
          typename PT,
          typename ET>
IF<IFType>* _i_col_factory_l1(char data_type,
                              U32 compress_id,
                              void*& data_ptr,
                              I32 data_size)
{
  switch (data_type)
  {
    case 'b':
      return _i_col_factory_l2<IF, IFImpl, IFType, PT, ET, I8>
        (compress_id, data_ptr, data_size);
    case 'B':
      return _i_col_factory_l2<IF, IFImpl, IFType, PT, ET, U8>
        (compress_id, data_ptr, data_size);
    case 'h':
      return _i_col_factory_l2<IF, IFImpl, IFType, PT, ET, I16>
        (compress_id, data_ptr, data_size);
    case 'H':
      return _i_col_factory_l2<IF, IFImpl, IFType, PT, ET, U16>
        (compress_id, data_ptr, data_size);
    case 'i':
      return _i_col_factory_l2<IF, IFImpl, IFType, PT, ET, I32>
        (compress_id, data_ptr, data_size);
    case 'I':
      return _i_col_factory_l2<IF, IFImpl, IFType, PT, ET, U32>
        (compress_id, data_ptr, data_size);
    default:
      return 0;  // TODO: exception throw
  }
}

template <template<typename IFType> class IF,
          template<typename IFType, class Impl> class IFImpl,
          typename IFType,
          typename ET>
IF<IFType>* _i_col_factory(char data_type,
                           U32 compress_id,
                           void*& data_ptr,
                           I32 data_size)
{
  if(data_size <= UCHAR_MAX)
  {
    return _i_col_factory_l1<IF, IFImpl, IFType, U8, ET>
      (data_type, compress_id, data_ptr, data_size);
  }
  if(data_size <= USHRT_MAX)
  {
    return _i_col_factory_l1<IF, IFImpl, IFType, U16, ET>
      (data_type, compress_id, data_ptr, data_size);
  }
  return _i_col_factory_l1<IF, IFImpl, IFType, U32, ET>
    (data_type, compress_id, data_ptr, data_size);
}
                                

// normal col factory
template <typename IFType>
Column<IFType>* i_col_factory(char data_type,
                              U32 compress_id,
                              void*& data_ptr,
                              I32 data_size)
{
  return _i_col_factory<Column, ColumnImpl, IFType, U8>
    (data_type, compress_id, data_ptr, data_size);
}

// sorted col factory
template <typename IFType>
SortedColumn<IFType>* i_scol_factory(char data_type,
                                     U32 compress_id,
                                     void*& data_ptr,
                                     I32 data_size)
{
  return _i_col_factory<SortedColumn, SortedColumnImpl, IFType, U8>
    (data_type, compress_id, data_ptr, data_size);
}

template <template<typename IFType> class IF,
          template<typename IFType, class Impl> class IFImpl,
          template<typename IFType> class TgtIF,
          typename IFType,
          typename PT,
          typename ET,
          typename DT>
IF<IFType>* _i_fcol_factory_l2(U32 compress_id,
                               void*& data_ptr,
                               I32 data_size,
                               TgtIF<IFType>* tgt)
{
  switch (compress_id)
  {
    case PLAIN:
      return new IFImpl<IFType, PlainImpl<DT> >(data_ptr, data_size, tgt);
    case RUN0:
      return new IFImpl<IFType, Run0Impl<DT, PT> >(data_ptr, data_size, tgt);
    case RUN1:
      return new IFImpl<IFType, Run1Impl<DT, PT> >(data_ptr, data_size, tgt);
    case ENUM:
      return new IFImpl<IFType, EnumImpl<DT, ET> >(data_ptr, data_size, tgt);
    default:
      return 0;  // TODO: exception throw
  }
}

template <template<typename IFType> class IF,
          template<typename IFType, class Impl> class IFImpl,
          template<typename IFType> class TgtIF,
          typename IFType,
          typename PT,
          typename ET>
IF<IFType>* _i_fcol_factory_l1(char data_type,
                               U32 compress_id,
                               void*& data_ptr,
                               I32 data_size,
                               TgtIF<IFType>* tgt)
{
  switch (data_type)
  {
    case 'b':
      return _i_fcol_factory_l2<IF, IFImpl, TgtIF, IFType, PT, ET, I8>
        (compress_id, data_ptr, data_size, tgt);
    case 'B':
      return _i_fcol_factory_l2<IF, IFImpl, TgtIF, IFType, PT, ET, U8>
        (compress_id, data_ptr, data_size, tgt);
    case 'h':
      return _i_fcol_factory_l2<IF, IFImpl, TgtIF, IFType, PT, ET, I16>
        (compress_id, data_ptr, data_size, tgt);
    case 'H':
      return _i_fcol_factory_l2<IF, IFImpl, TgtIF, IFType, PT, ET, U16>
        (compress_id, data_ptr, data_size, tgt);
    case 'i':
      return _i_fcol_factory_l2<IF, IFImpl, TgtIF, IFType, PT, ET, I32>
        (compress_id, data_ptr, data_size, tgt);
    case 'I':
      return _i_fcol_factory_l2<IF, IFImpl, TgtIF, IFType, PT, ET, U32>
        (compress_id, data_ptr, data_size, tgt);
    default:
      return 0;  // TODO: exception throw
  }
}

template <template<typename IFType> class IF,
          template<typename IFType, class Impl> class IFImpl,
          template<typename IFType> class TgtIF,
          typename IFType,
          typename ET>
IF<IFType>* _i_fcol_factory(char data_type,
                            U32 compress_id,
                            void*& data_ptr,
                            I32 data_size,
                            TgtIF<IFType>* tgt)
{
  if(data_size <= UCHAR_MAX)
  {
    return _i_fcol_factory_l1<IF, IFImpl, TgtIF, IFType, U8, ET>
      (data_type, compress_id, data_ptr, data_size, tgt);
  }
  if(data_size <= USHRT_MAX)
  {
    return _i_fcol_factory_l1<IF, IFImpl, TgtIF, IFType, U16, ET>
      (data_type, compress_id, data_ptr, data_size, tgt);
  }
  return _i_fcol_factory_l1<IF, IFImpl, TgtIF, IFType, U32, ET>
    (data_type, compress_id, data_ptr, data_size, tgt);
}

// normal fcol factory
template <typename IFType>
FKeyColumn<IFType>* i_fcol_factory(char data_type,
                                   U32 compress_id,
                                   void*& data_ptr,
                                   I32 data_size,
                                   SortedColumn<IFType>* tgt)
{
  return _i_fcol_factory<FKeyColumn, FKeyColumnImpl, SortedColumn,
                         IFType, U8>
    (data_type, compress_id, data_ptr, data_size, tgt);
}

// sorted fcol factory
template <typename IFType>
SortedFKeyColumn<IFType>* i_sfcol_factory(char data_type,
                                          U32 compress_id,
                                          void*& data_ptr,
                                          I32 data_size,
                                          SortedColumn<IFType>* tgt)
{
  return _i_fcol_factory<SortedFKeyColumn, SortedFKeyColumnImpl, SortedColumn,
                         IFType, U8>
    (data_type, compress_id, data_ptr, data_size, tgt);
}

// struct col factory
template <U32 bytes>
Column<std::string>* s_col_factory(char data_type,
                                   U32 compress_id,
                                   void*& data_ptr,
                                   I32 data_size)
{
  // struct implementation now ignores data_type and compress_id
  return new ColumnImpl<std::string, StructImpl<bytes> >(data_ptr, data_size);
}

// blob col factory
template <U32 align>
Column<std::string>* b_col_factory(char data_type,
                                   U32 compress_id,
                                   void*& data_ptr,
                                   I32 data_size)
{
  switch (data_type)
  {
    case 's':
      return new ColumnImpl<std::string, BlobImpl<U16, align> >
        (data_ptr, data_size);
    case 'S':
      return new ColumnImpl<std::string, BlobImpl<U32, align> >
        (data_ptr, data_size);
    default:
      return 0;  // TODO: exception throw
  }
}

}
#endif
