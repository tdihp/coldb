#ifndef INCLUDED_COLDB_FACTORY_HPP
#define INCLUDED_COLDB_FACTORY_HPP

#include "types.hpp"
#include "column.hpp"

namespace coldb
{

template <typename IFType>
Column<IFType>* column_factory(char data_type, U8 compress_id)
{
  // TODO: fill this
}

}
#endif
