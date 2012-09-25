#ifndef INCLUDED_COLDB_FACTORY_HPP
#define INCLUDED_COLDB_FACTORY_HPP

#include "types.hpp"
#include "column.hpp"

namespace coldb
{

template <typename IFType, typename PT, typename ET, typename DT>
Column<IFType>* _int_column_factory_l1(E_COMPRESS compress_id,
                                   void* data_ptr,
                                   I32 data_size)
{
  switch (compress_id)
    case E_COMPRESS.PLAIN:
      return new ColumnImpl<IFType, PlainImpl<DT>>(data_ptr, data_size);
    case E_COMPRESS.RUN0:
      return new ColumnImpl<IFType, Run0Impl<DT, PT>>(data_ptr, data_size);
    case E_COMPRESS.RUN1:
      return new ColumnImpl<IFType, Run1Impl<DT, PT>>(data_ptr, data_size);
    case E_COMPRESS.ENUM:
      return new ColumnImpl<IFType, EnumImpl<DT, ET>>(data_ptr, data_size);
    default:
      break;  // TODO: exception throw
}

template <typename IFType, typename PT, typename ET>
Column<IFType>* int_column_factory(char data_type,
                               E_COMPRESS compress_id,
                               void* data_ptr,
                               I32 data_size)
{
  switch (data_type)
    case 'b':
      return _int_column_factory_l1<IFType, PT, ET, I8>(compress_id,
                                                        data_ptr,
                                                        data_size);
    case 'B':
      return _int_column_factory_l1<IFType, PT, ET, U8>(compress_id,
                                                        data_ptr,
                                                        data_size);
    case 'h':
      return _int_column_factory_l1<IFType, PT, ET, I16>(compress_id,
                                                         data_ptr,
                                                         data_size);
    case 'H':
      return _int_column_factory_l1<IFType, PT, ET, U16>(compress_id,
                                                         data_ptr,
                                                         data_size);
    case 'i':
      return _int_column_factory_l1<IFType, PT, ET, I32>(compress_id,
                                                         data_ptr,
                                                         data_size);
    case 'I':
      return _int_column_factory_l1<IFType, PT, ET, U32>(compress_id,
                                                         data_ptr,
                                                         data_size);
    default:
      break;  // TODO: exception throw
}

}
#endif
