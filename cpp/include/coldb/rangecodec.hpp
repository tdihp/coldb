#ifndef INCLUDED_COLDB_RANGECODEC_HPP
#define INCLUDED_COLDB_RANGECODEC_HPP

#include "types.hpp"
#include <stdio.h>

namespace coldb{

struct RangeCore
{
  static const U32 CODE_BITS = 32;
  static const U32 SHIFT_BITS = CODE_BITS - 9;
  static const U32 EXTRA_BITS = ((CODE_BITS-2) % 8 + 1);
  static const U32 TOP_VAL = 1 << (CODE_BITS - 1);
  static const U32 BOTTOM_VAL = TOP_VAL >> 8;

  U32 lo_, range_, help_;
  U8 cbuff_;

  RangeCore(U32 lo, U32 range, U32 help, U8 cbuff)
    : lo_(lo),
      range_(range),
      help_(help),
      cbuff_(cbuff) {}
};

template<typename Stream, U32 FREQ_BITS>
struct REncoder : public RangeCore
{
  Stream* buf_; //served as IO

  REncoder(Stream* buf)
    : RangeCore(0, TOP_VAL, 0, 0), buf_(buf)
  {}

  // normalize
  void norm()
  {
    while(range_ <= BOTTOM_VAL)
    {
      if (lo_ < ((U32)0xff << SHIFT_BITS)) // normal path
      {
        buf_->put(cbuff_);
        for(; help_; --help_)
        {
          buf_->put(0xff);
        }
        cbuff_ = (U8)(lo_ >> SHIFT_BITS);
      }
      else // overflow path
      {
        if(lo_ & TOP_VAL) // first  bit is 1
        {
          buf_->put(cbuff_ + 1); // add 1 because???
          for(; help_; --help_)
          {
            buf_->put(0); // related to +1 ?
          }
          cbuff_ = (U8)(lo_ >> SHIFT_BITS);
        }
        else // first bit is 0
        {
          ++help_;
        }
      }
      range_ <<= 8;
      lo_  = (lo_ << 8) & (TOP_VAL - 1); // masking
    }
  }

  // encode a symbol
  void enc(U32 cmin, U32 csize)
  {
    U32 r;
    U32 tmp;
    norm();
    r = range_ >> FREQ_BITS;
    tmp = r * cmin;
    lo_ += tmp; // overflow from here?
    if((cmin + csize) >> FREQ_BITS)
    {
      range_ -= tmp;  
    }
    else
    {
      range_ = r * csize;
    }
  }

  void flush()
  {
    U32 tmp;
    norm();

    tmp = (lo_ >> SHIFT_BITS) + 1;

    if(tmp > 0xff) // overflow
    {
      buf_->put(cbuff_ + 1);
      for(; help_; --help_)
      {
        buf_->put(0);
      }
    }
    else
    {
      buf_->put(cbuff_);
      for(; help_; --help_)
      {
        buf_->put(0xff);
      }
    }
    buf_->put(tmp & 0xff);
  }
};

template<typename Stream, U32 FREQ_BITS>
struct RDecoder : public RangeCore
{
  Stream* buf_; //served as IO

  RDecoder(Stream* buf)
    : RangeCore(0, 0, 0, 0), buf_(buf)
  {
    cbuff_ = buf_->get(); // at least 1 bit input required
    lo_ = cbuff_ >> (8 - EXTRA_BITS);
    range_ = 1 << EXTRA_BITS;
  }

  void norm()
  {
    while (range_ <= BOTTOM_VAL)
    {
      lo_ = (lo_ << 8) | ((cbuff_ << EXTRA_BITS) & 0xff);
      cbuff_ = buf_->get();
      lo_ |= cbuff_ >> (8 - EXTRA_BITS);
      range_ <<= 8;
    }
  }

  U32 mid()
  {
    U32 tmp;
    norm();
    help_ = range_ >> FREQ_BITS;
    tmp = lo_ / help_; // true division!
    return ((tmp>>FREQ_BITS) ? ((1 << FREQ_BITS) - 1) : tmp);
  }

  void dec(U32 cmin, U32 csize)
  {
    U32 tmp;
    tmp = help_ * cmin;
    lo_ -= tmp;
    if(!((cmin + csize) >> FREQ_BITS))
    {
      range_ = help_ * csize;
    }
    else
    {
      range_ -= tmp;
    }
  }
};

};
#endif
