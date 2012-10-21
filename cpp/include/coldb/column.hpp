#ifndef INCLUDED_COLDB_COLUMN_HPP
#define INCLUDED_COLDB_COLUMN_HPP

#include <algorithm>
#include <string>
#include "coldb/types.hpp"

namespace coldb
{

template <unsigned int bytes>
inline void* aligned(void* ptr)
{
  // TODO: assert 2, 4
  U32 align_mask = bytes - 1;
  UPT u_ptr = (UPT)ptr;
  UPT tail = u_ptr & align_mask;
  if(tail)
  {
    return (void*) (u_ptr + bytes - tail);
  }
  return ptr;
}

template <>
inline void* aligned<1>(void* ptr) {return ptr;}


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
class ColumnImpl : virtual public Column<IFType>
{
protected:
  Impl impl_;
public:
  ColumnImpl(void*& data_ptr, I32 data_size)
    : Column<IFType>(),
      impl_(data_ptr, data_size)
  {}

  I32 get_size() {return impl_.data_size_;}

  IFType get(I32 rowid) {return impl_.get(rowid);}
};

// abstract interface of sorted column for findings
template <typename IFType>
class SortedColumn : virtual public Column<IFType> {
public:
  virtual I32 find(IFType var) = 0;  // find the row of target value
};

template <typename IFType, class Impl>
class SortedColumnImpl
  : virtual public SortedColumn<IFType>, public ColumnImpl<IFType, Impl>
{
private:
  typedef ColumnImpl<IFType, Impl> Base;
public:
  SortedColumnImpl(void*& data_ptr, I32 data_size)
    :Base(data_ptr, data_size)
  {}

  I32 find(IFType var){return Base::impl_.find(var);}
};

template <typename IFType>
class FKeyColumn : virtual public Column<IFType>
{
public:
  // virtual I32 find_by_tgt_row(I32 tgt_row) = 0;
  virtual I32 get_tgt_row(I32 rowid) = 0;
};

template <typename IFType, class Impl>
class FKeyColumnImpl : virtual public FKeyColumn<IFType>
{
protected:
  Impl impl_;
  SortedColumn<IFType>* tgt_;
public:
  FKeyColumnImpl(void*& data_ptr, I32 data_size, SortedColumn<IFType>* tgt)
    : impl_(data_ptr, data_size), tgt_(tgt)
  {}
  I32 get_size() {return impl_.data_size_;}
  I32 get_tgt_row(I32 rowid) {return impl_.get(rowid);}
  IFType get(I32 rowid) {return tgt_->get(get_tgt_row(rowid));}
};

template <typename IFType>
class SortedFKeyColumn
  : virtual public SortedColumn<IFType>, virtual public FKeyColumn<IFType>
{
public:
  virtual I32 find_dest_row(I32 tgt_row) = 0;
};

template <typename IFType, class Impl>
class SortedFKeyColumnImpl
  : virtual public SortedFKeyColumn<IFType>,
    public FKeyColumnImpl<IFType, Impl>
{
private:
  typedef FKeyColumnImpl<IFType, Impl> Base;
public:
  SortedFKeyColumnImpl(void*& data_ptr, I32 data_size, SortedColumn<IFType>* tgt)
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

  PlainImpl(void*& data_ptr, I32 data_size)
    : data_ptr_((DT*)data_ptr), data_size_(data_size)
  {
    //int dbg_size = (char*)aligned<sizeof(ALIGN_T)>((void*)(data_ptr_ + data_size_)) - (char*)data_ptr;
    data_ptr = aligned<sizeof(ALIGN_T)>((void*)(data_ptr_ + data_size_));
  }
  // TODO: add no such row situation
  DT get(I32 rowid) {return data_ptr_[rowid];}

  I32 find(DT var)
  {
    DT* end = data_ptr_ + data_size_;
    DT* i = std::lower_bound(data_ptr_, end, var);
    if((end != i) && (*i == var))
    {
      return i - data_ptr_;
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

  Run0Impl(void*& data_ptr, I32 data_size) : data_size_(data_size)
  {
    run_cnt_ = *((PT*)data_ptr);
    run_ptr_ = ((PT*)data_ptr) + 1;
    data_ptr_ = (DT*)aligned<sizeof(DT)>((void*)(run_ptr_ + run_cnt_));
    //int dbg_size = (char*)aligned<sizeof(ALIGN_T)>((void*)(data_ptr_ + run_cnt_)) - (char*)data_ptr;
    data_ptr = aligned<sizeof(ALIGN_T)>((void*)(data_ptr_ + run_cnt_));
  }

  DT get(I32 rowid)
  {
    // TODO: add no such row situation
    // find rowid in run_ptr
    PT* runid = std::lower_bound(run_ptr_, run_ptr_ + run_cnt_, rowid);

    if(*runid != rowid)
    {
      --runid;
    }
    // rtn data from data_ptr
    return data_ptr_[runid - run_ptr_];
  }

  I32 find(DT var)
  {
    DT* end = data_ptr_ + run_cnt_;
    DT* dptr = std::lower_bound(data_ptr_, end, var);
    if((dptr != end) && (*dptr == var))
    {
      return run_ptr_[dptr - data_ptr_];
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
  Run1Impl(void*& data_ptr, I32 data_size): Run0Impl<DT, PT>(data_ptr, data_size)
  {}
  DT get(I32 rowid)
  {
    // TODO: add no such row situation
    // find rowid in run_ptr
    PT* runid = std::lower_bound(Base::run_ptr_,
                                 Base::run_ptr_ + Base::run_cnt_,
                                 rowid);

    if(*runid != rowid)
    {
      --runid;
    }
    return Base::data_ptr_[runid - Base::run_ptr_] + (rowid - *runid);
  }

  I32 find(DT var)
  {
    DT* end = Base::data_ptr_ + Base::run_cnt_;
    DT* dptr = std::lower_bound(Base::data_ptr_, end, var);

    if((dptr == end) || (*dptr != var))
    {
      if(dptr == Base::data_ptr_)
      {
        return -1;
      }
      else
      {
        --dptr;
      }
    }

    I32 diff = var - *dptr;
    I32 i = dptr - Base::data_ptr_;
    PT* this_run = Base::run_ptr_ + i;
    I32 runlen;

    //situation of 12333345 find(3), tricky part of this compress
    if((i > 0) && (!diff))
    {
      if((*this_run - *(this_run - 1)) >= (var - *(dptr - 1)))
      {
        return (*this_run - 1);
      }
    }

    // get length of this run
    if(i == (Base::run_cnt_ - 1))
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

  EnumImpl(void*& data_ptr, I32 data_size) : data_size_(data_size)
  {
    enum_cnt_ = *((ET*)data_ptr);
    new_val_ptr_ = ((ET*)data_ptr) + 1;
    enum_ptr_ = (DT*)aligned<sizeof(DT)>((void*)(new_val_ptr_ + data_size_));
    //int dbg_size = (char*)aligned<sizeof(ALIGN_T)>((void*)(enum_ptr_ + enum_cnt_)) - (char*)data_ptr;
    data_ptr = aligned<sizeof(ALIGN_T)>((void*)(enum_ptr_ + enum_cnt_));
  }

  DT get(I32 rowid)
  {
    return enum_ptr_[new_val_ptr_[rowid]];
  }

  // find is oddly used, whatever
  I32 find(DT var)
  {
    DT* enum_i = std::lower_bound(enum_ptr_, enum_ptr_ + enum_cnt_, var);
    if(*enum_i != var)
    {
      return -1;
    }

    return std::lower_bound(new_val_ptr_, new_val_ptr_ + data_size_,
      enum_i - enum_ptr_) - new_val_ptr_;
  }
};

template <typename DT, typename PT, typename FT>
struct FrameImpl
{
  I32 data_size_;
  I32 frame_cnt_;
  PT* row_ptr_;
  DT* frame_ptr_;
  FT* val_ptr_;

  FrameImpl(void*& data_ptr, I32 data_size)
    : data_size_(data_size)
  {
    frame_cnt_ = *((PT*)data_ptr);
    row_ptr_ = (PT*)data_ptr + 1;
    frame_ptr_ = (DT*)(aligned<sizeof(DT)>((void*)(row_ptr_ + frame_cnt_)));
    val_ptr_ = (FT*)(frame_ptr_ + frame_cnt_);  // NOTE: FT is supposed to be smaller, no align needed
    //int dbg_size = (char*)aligned<sizeof(ALIGN_T)>((void*)(val_ptr_ + data_size_)) - (char*)data_ptr;
    data_ptr = aligned<sizeof(ALIGN_T)>((void*)(val_ptr_ + data_size_));
  }

  DT get(I32 rowid)
  {
    // find the frame of the row
    PT* i_row = std::lower_bound(row_ptr_, row_ptr_ + frame_cnt_, rowid);
    if(*i_row != rowid)
    {
      --i_row;
    }
    I32 i = i_row - row_ptr_;
    DT frame = frame_ptr_[i];
    return frame + val_ptr_[rowid];
  }

  I32 find(DT var)
  {
    DT* src_end = frame_ptr_ + frame_cnt_;
    DT* i_frame = std::lower_bound(frame_ptr_, frame_ptr_ + frame_cnt_, var);
    if(i_frame == src_end)
    {
      --i_frame;
    }
    else
    {
      if(*i_frame == var)
      {
        return row_ptr_[i_frame - frame_ptr_];
      }
      if(i_frame == frame_ptr_)
      {
        return -1;
      }
      --i_frame;
    }
    U32 diff = var - *i_frame;
    if (diff >= 0x10000)  // NOTE: hard coded for U16 FT
    {
      return -2;
    }
    I32 fi = i_frame - frame_ptr_;
    FT* begin = val_ptr_ + row_ptr_[fi];
    FT* end;
    if(fi == frame_cnt_ - 1)
    {
      end = val_ptr_ + data_size_;
    }
    else
    {
      end = val_ptr_ + row_ptr_[fi + 1];
    }
    FT* res = std::lower_bound(begin, end, diff);
    if(res == end)
    {
      return -3;
    }
    if(*res != diff)
    {
      return -4;
    }
    return res - val_ptr_;
  }
};

template <U32 bytes>
struct StructImpl
{
  I32 data_size_;
  char* data_ptr_;

  StructImpl(void*& data_ptr, I32 data_size)
    : data_size_(data_size), data_ptr_((char*)data_ptr)
  {
    //int dbg_size = (char*)aligned<sizeof(ALIGN_T)>((void*)(data_ptr_ + (data_size_ * bytes))) - (char*)data_ptr;
    data_ptr = aligned<sizeof(ALIGN_T)>((void*)(data_ptr_ + (data_size_ * bytes)));
  }

  std::string get(I32 rowid)
  {
    return std::string(data_ptr_ + (rowid * bytes), bytes);
  }
};

template <typename BPT, U32 align>
struct BlobImpl
{
  I32 data_size_;
  U32 blob_size_;  // aligned blob size
  BPT* offset_ptr_;  // aligned offset
  char* blob_ptr_;  // raw data

  BlobImpl(void*& data_ptr, I32 data_size)
    : data_size_(data_size)
  {
    blob_size_ = *((BPT*)data_ptr);
    offset_ptr_ = ((BPT*)data_ptr) + 1;
    blob_ptr_ = (char*)(offset_ptr_ + data_size_);
    //int dbg_size = (char*)aligned<sizeof(ALIGN_T)>((void*)(blob_ptr_ + (blob_size_ * align))) - (char*)data_ptr;
    data_ptr = aligned<sizeof(ALIGN_T)>((void*)(blob_ptr_ + (blob_size_ * align)));
  }

  std::string get(I32 rowid)
  {
    U32 aligned_size;
    U32 offset = offset_ptr_[rowid];
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
