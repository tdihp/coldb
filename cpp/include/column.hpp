#ifndef INCLUDED_COLDB_COLUMN_HPP
#define INCLUDED_COLDB_COLUMN_HPP

#include <algorithm>
#include "types.hpp"

namespace coldb{

// abstract interface of all column objects
// IFType: type of interface
// ACType: type of actual storage
template <typename IFType>
class Column{
private:
  const DATA_PTR data_ptr_;
public:
  const I32 size_;
public:
  Column(const DATA_PTR data_ptr, const I32 size)
    : data_ptr_(data_ptr), size_(size) {}
  virtual ~Column(){}
  virtual IFType get(I32 rowid) = 0;  // get the item in rowid row
};

// abstract interface of sorted column for findings
template <typename IFType>
class SortedColumn : public virtual Column<IFType, ACType> {
  virtual I32 find(IFType var);  // find the row of target value
};


template <typename IFType, typename ACType>
class PlainColumn : public Column<IFType>{
public:
  IFType get(I32 rowid) {return (IFType)(((ACType*)ptr)[i]);}
};

template <typename IFType, typename ACType>
class SortedPlainColumn
  : public PlainColumn<IFType, ACType>, public SortedColumn<IFType>
{
public:
  I32 find(IFType var)
  {
    ACType* data = (ACType*)data_ptr_;
    I32 i = std::lower_bound(data, data + size_, (ACType)var);
    if(data[i] == (ACType)var)
    {
      return i;
    }
    return -1;
  }
};

template <typename IFType, typename ACType>
class Run0Column : public Column<IFType>{
public:
  IFType get(I32 rowid) {return (IFType)(((ACType*)ptr)[i]);}
};

}
#endif
