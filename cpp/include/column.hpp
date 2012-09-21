#ifndef INCLUDED_COLDB_COLUMN_HPP
#define INCLUDED_COLDB_COLUMN_HPP

#include <algorithm>
#include "types.hpp"

namespace coldb{

// abstract interface of all column objects
// IFType: type of interface
// ACType: type of actual storage
template <typename IFType>
class Column
{
public:
  Column() {}
  virtual ~Column() {}
  virtual I32 get_size() = 0;
  virtual IFType get(I32 rowid) = 0;  // get the item in rowid row
};

template <typename IFType, class Impl>
class ColumnImpl : public Column<IFType>
{
private:
  Impl impl_;
public:
  ColumnImpl(void* data_ptr, I32 data_size)
    : Column(),
      impl_(data_ptr, data_size)
  {}
  
  I32 get_size() {return impl_.data_size_;}
  
  IFType get(I32 rowid) {return impl_.get(rowid);}
};

// abstract interface of sorted column for findings
template <typename IFType>
class SortedColumn : public virtual Column<IFType, ACType> {
public:
  virtual I32 find(IFType var) = 0;  // find the row of target value
};

template <typename IFType, class Impl>
class SortedColumnImpl
  : public SortedColumn<IFType>, public ColumnImpl<IFType, Impl>
{
public:
  SortedColumnImpl(void* data_ptr, I32 data_size)
    : SortedColumn(),
      ColumnImpl(data_ptr, data_size)
  {}
  
  I32 find(IFType var){return impl_.find(var);}
};

template <typename IFType>
class FKeyColumn : public virtual Column<IFType>
{
public:
  // virtual I32 find_by_tgt_row(I32 tgt_row) = 0;
  virtual I32 get_tgt_row(I32 rowid) = 0;
};

template <typename IFType, class Impl, class TgtImpl>
class FKeyColumnImpl : public FKeyColumn<IFType>
{
private:
  Impl impl_;
  TgtImpl tgt_impl_;
public:
  FKeyColumnImpl(void* data_ptr, I32 data_size, TgtImpl& tgt_impl)
    : impl_(data_ptr, data_size), tgt_impl_(tgt_impl)
  {}
  
  I32 get_tgt_row(I32 rowid) {return impl_.get(rowid);}
  
  IFType get(I32 rowid) {return tgt_impl_.get(get_tgt_row(rowid));}
};

template <typename IFType>
class SortedFKeyColumn
  : public virtual SortedColumn<IFType>, public virtual FKeyColumn<IFType>
{
public:
  virtual I32 find_dest_row(I32 tgt_row) = 0;
};

template <typename IFType, class Impl, class TgtImpl>
class SortedFKeyColumnImpl
  : public SortedFKeyColumn<IFType>,
    public FKeyColumnImpl<IFType, Impl, TgtImpl>
{
public:
  SortedFKeyColumnImpl(void* data_ptr, I32 data_size, TgtImpl& tgt_impl)
    : SortedFKeyColumn(),
      FKeyColumnImpl(data_ptr, data_size, tgt_impl)
  {}
  
  I32 find_dest_row(I32 tgt_row) {return impl_.find(tgt_row);}
  
  I32 find(IFType var) {return impl_.find(tgt_impl_.find(var));}
};

template <typename DT>
struct PlainImpl
{
  DT* data_ptr_;
  I32 data_size_;
  
  PlainImpl(DT* data_ptr, I32 data_size)
    : data_ptr_(data_ptr), data_size_(data_size)
  {}

  DT get(I32 rowid) {return data_ptr_[i];}

  I32 find(DT var)
  {
    I32 i = std::lower_bound(data_ptr_, data_ptr_ + data_size_, var);
    if(data_ptr_[i] == var)
    {
      return i;
    }
    return -1;
  }
};


template <typename DT, typename PT>
struct Run0Impl{
};

}
#endif
