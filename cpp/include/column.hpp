#ifndef INCLUDED_COLDB_COLUMN_HPP
#define INCLUDED_COLDB_COLUMN_HPP

#include <algorithm>
#include <string>
#include "types.hpp"

namespace coldb
{

template <typename T>
inline void* aligned(void* ptr)
{
  U32 align_mask = sizeof(T) - 1;
  U32 u_ptr = (U32)ptr;
  U32 tail = u_ptr & align_mask;
  if(tail)
  {
    return (void*) (u_ptr + sizeof(T) - tail);
  }
  return ptr;
}

template <>
inline void* aligned<U8>(void* ptr) {return ptr;}

template <>
inline void* aligned<I8>(void* ptr) {return ptr;}

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
protected:
  Impl impl_;
public:
  ColumnImpl(void* data_ptr, I32 data_size)
    : Column<IFType>(),
      impl_(data_ptr, data_size)
  {}
  
  I32 get_size() {return impl_.data_size_;}
  
  IFType get(I32 rowid) {return impl_.get(rowid);}
};

// abstract interface of sorted column for findings
template <typename IFType>
class SortedColumn : public virtual Column<IFType> {
public:
  virtual I32 find(IFType var) = 0;  // find the row of target value
};

template <typename IFType, class Impl>
class SortedColumnImpl
  : public SortedColumn<IFType>, public ColumnImpl<IFType, Impl>
{
private:
  typedef ColumnImpl<IFType, Impl> Base;
public:
  SortedColumnImpl(void* data_ptr, I32 data_size)
    : SortedColumn<IFType>(),
      Base(data_ptr, data_size)
  {}
  
  I32 find(IFType var){return Base::impl_.find(var);}
};

template <typename IFType>
class FKeyColumn : public virtual Column<IFType>
{
public:
  // virtual I32 find_by_tgt_row(I32 tgt_row) = 0;
  virtual I32 get_tgt_row(I32 rowid) = 0;
};

template <typename IFType, class Impl>
class FKeyColumnImpl : public FKeyColumn<IFType>
{
protected:
  Impl impl_;
  SortedColumn<IFType>* tgt_;
public:
  FKeyColumnImpl(void* data_ptr, I32 data_size, SortedColumn<IFType>* tgt)
    : impl_(data_ptr, data_size), tgt_(tgt)
  {}
  
  I32 get_tgt_row(I32 rowid) {return impl_.get(rowid);}
  
  IFType get(I32 rowid) {return tgt_->get(get_tgt_row(rowid));}
};

template <typename IFType>
class SortedFKeyColumn
  : public virtual SortedColumn<IFType>, public virtual FKeyColumn<IFType>
{
public:
  virtual I32 find_dest_row(I32 tgt_row) = 0;
};

template <typename IFType, class Impl>
class SortedFKeyColumnImpl
  : public SortedFKeyColumn<IFType>,
    public FKeyColumnImpl<IFType, Impl>
{
private:
  typedef FKeyColumnImpl<IFType, Impl> Base;
public:
  SortedFKeyColumnImpl(void* data_ptr, I32 data_size, SortedColumn<IFType>* tgt)
    : SortedFKeyColumn<IFType>(),
      Base(data_ptr, data_size, tgt)
  {}
  
  I32 find_dest_row(I32 tgt_row) {return Base::impl_.find(tgt_row);}
  
  I32 find(IFType var) {return Base::impl_.find(Base::tgt_->find(var));}
};

template <typename DT>
struct PlainImpl
{
  DT* data_ptr_;
  I32 data_size_;
  
  PlainImpl(DT* data_ptr, I32 data_size)
    : data_ptr_(data_ptr), data_size_(data_size)
  {}

  DT get(I32 rowid) {return data_ptr_[rowid];}

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
struct Run0Impl
{
  I32 data_size_;
  I32 run_cnt_;
  PT* run_ptr_;
  DT* data_ptr_;
  
  Run0Impl(void* data_ptr, I32 data_size) : data_size_(data_size)
  {
    run_cnt_ = *((PT*)data_ptr);
    run_ptr_ = ((PT*)data_ptr) + 1;
    data_ptr_ = aligned<DT>(run_ptr_ + run_cnt_);
  }
  
  DT get(I32 rowid)
  {
    // find rowid in run_ptr
    I32 runid = std::lower_bound(run_ptr_, run_ptr_ + run_cnt_, rowid);
    
    if(run_ptr_[runid] != rowid)
    {
      --runid;
    }
    // rtn data from data_ptr
    return data_ptr_[runid];
  }
  
  I32 find(DT var)
  {
    I32 runid = std::lower_bound(data_ptr_, data_ptr_ + run_cnt_, var);
    if(data_ptr_[runid] == var)
    {
      return run_ptr_[runid];
    }
    return -1;
  }
};

template <typename DT, typename PT>
struct Run1Impl : public Run0Impl<DT, PT>
{
private:
  typedef Run0Impl<DT, PT> Base;
public:
  DT get(I32 rowid)
  {
    // find rowid in run_ptr
    I32 runid = std::lower_bound(Base::run_ptr_,
                                 Base::run_ptr_ + Base::run_cnt_,
                                 rowid);
    
    if(Base::run_ptr_[runid] != rowid)
    {
      --runid;
    }
    return Base::data_ptr_[runid] + (rowid - Base::run_ptr_[runid]);
  }
  
  I32 find(DT var)
  {
    I32 runid = std::lower_bound(Base::data_ptr_, Base::data_ptr_ + Base::run_cnt_, var);
    DT* this_run = Base::run_ptr_ + runid;
    I32 runlen;
    I32 diff = var - Base::data_ptr_[runid];
    // get length of this run
    if(runid == (Base::run_cnt_ - 1))
    {
      runlen = Base::data_size_ - *this_run;
    }
    else
    {
      runlen = *(this_run + 1) - *this_run;
    }
    
    if(diff < runlen)
    {
      return *this_run + diff;
    }
    return -1;
  }
};

template <typename DT, typename ET>
struct EnumImpl
{
  I32 data_size_;
  I32 enum_cnt_;
  ET* new_val_ptr_;
  DT* enum_ptr_;
  
  EnumImpl(void* data_ptr, I32 data_size) : data_size_(data_size)
  {
    enum_cnt_ = *((ET*)data_ptr);
    new_val_ptr_ = ((ET*)data_ptr) + 1;
    enum_ptr_ = aligned<DT>(new_val_ptr_ + data_size_);
  }
  
  DT get(I32 rowid)
  {
    return enum_ptr_[new_val_ptr_[rowid]];
  }
  
  // find is oddly used, whatever
  I32 find(DT var)
  {
    I32 enum_i = std::lower_bound(enum_ptr_, enum_ptr_ + enum_cnt_, var);
    if(enum_ptr_[enum_i] != var)
    {
      return -1;
    }
    
    return std::lower_bound(new_val_ptr_, new_val_ptr_ + data_size_, enum_i);
  }
};

template <U32 bytes>
struct StructImpl
{
  I32 data_size_;
  void* data_ptr_;
  
  StructImpl(void* data_ptr, I32 data_size)
    : data_size_(data_size), data_ptr_(data_ptr)
  {}
  
  std::string get(I32 rowid)
  {
    return std::string(data_ptr_ + (rowid * bytes), bytes);
  }
};

template <typename PT, U32 align>
struct BlobImpl
{
  I32 data_size_;
  I32 blob_size_;  // aligned blob size
  PT* offset_ptr_;  // aligned offset
  char* blob_ptr_;  // raw data
  
  BlobImpl(void* data_ptr, I32 data_size)
    : data_size_(data_size)
  {
    blob_size_ = *((PT*)data_ptr);
    offset_ptr_ = ((PT*)data_ptr) + 1;
    blob_ptr_ = offset_ptr_ + data_size_;
  }
  
  std::string get(I32 rowid)
  {
    I32 aligned_size;
    I32 offset = offset_ptr_[rowid];
    if(rowid == data_size_ - 1)
    {
      aligned_size = blob_size_ - offset;
    }
    else
    {
      aligned_size = offset_ptr_[rowid + 1] - offset;
    }
    
    return std::string(blob_ptr_ + (offset * align), aligned_size * align);
  }
};

}
#endif
