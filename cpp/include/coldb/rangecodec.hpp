#ifndef INCLUDED_COLDB_RANGECODEC_HPP
#define INCLUDED_COLDB_RANGECODEC_HPP

#include "types.hpp"


namespace coldb{

template<U32 RANGE_SIZE, typename STREAM, typename CT>
class RangeCore
{
public:
  RangeCore(STREAM* buf)
    : buf_(buf),
      lo_(0),
      mid_(0),
      hi_(MASK)
  {}
  ~RangeCore(){}
  void update(U32 cmin, U32 cmax)
  {
    CT range = hi_ - lo_;
    hi_ = lo_ + ((range * cmax) >> RANGE_SIZE);
    lo_ += ((range * cmin) >> RANGE_SIZE) + 1;
  }

  void enc(U32 cmin, U32 cmax)
  {
    update(cmin, cmax);
    if((hi_ - lo_) < RANGE_LIMIT)
    {
      hi_ = lo_;
    }
    while(!((lo_ ^ hi_) >> SHIFT))
    {
      buf_->put((U8)(lo_ >> SHIFT));
      lo_ <<= 8;
      hi_ = (hi_ << 8) | 0xff;
    }
    lo_ &= MASK;
    hi_ &= MASK;
  }

  void dec(U32 cmin, U32 cmax)
  {
    update(cmin, cmax);
    if((hi_ - lo_) < RANGE_LIMIT)
    {
      hi_ = lo_;
    }
    while(!((lo_ ^ hi_) >> SHIFT))
    {
      lo_ <<= 8;
      hi_ = (hi_ << 8) | 0xff;
      mid_ = (mid_ << 8) | (U8)(buf_->get());
    }
    lo_ &= MASK;
    hi_ &= MASK;
    mid_ &= MASK;
  }

  void encFlush()
  {
    lo_ += 1;
    for(U32 i = BYTES_IN_BUFFER; i; --i)
    {
      buf_->put((U8)(lo_ >> SHIFT));
      lo_ <<= 8;
    }
  }

  void decInit()
  {
	  for(U32 i = BYTES_IN_BUFFER; i; --i)
	  {
		  mid_ = (mid_ << 8) | (U8)(buf_->get());
	  }
  }

  U32 decGetMid()
  {
    return ((mid_ - lo_) << RANGE_SIZE) / (hi_ - lo_);
  }

private:
  static const U32 BYTES_IN_BUFFER = (sizeof(CT) * 8 - RANGE_SIZE) / 8;
  static const U32 SHIFT = (BYTES_IN_BUFFER - 1) * 8;
  static const CT RANGE_LIMIT = (CT)(1) << RANGE_SIZE;
  static const CT MASK = ((CT)(1) << (BYTES_IN_BUFFER * 8)) - 1;
  STREAM* buf_; //served as IO
  CT lo_, hi_, mid_;
};

};
#endif
