#ifndef INCLUDED_COLDB_COLUMN_HPP
#define INCLUDED_COLDB_COLUMN_HPP

#include "types.hpp"

// abstract interface of all column objects
template <typename DataType>
class Column{
private:
  const DATA_PTR data_ptr;
public:
  const PKGPT size;
public:
  Column(const DATA_PTR data_ptr, const PKGPT size) : data_ptr(data_ptr), size(size) {};
  virtual ~Column(){}
  virtual PKGPT get_size() = 0;  // get size of Column
  virtual DataType get(PKGPT rowid) = 0;  // get the item in rowid row
};

// abstract interface of sorted column for findings
template <typename DataType>
class SortedColumn : public virtual Column<DataType> {
  virtual PKGPT find(DataType var);  // find the row of target value
};

template <typename DataType>
class PlainColumn : public Column<DataType>{
private:
  const DataType* ptr;
  const COLPT size;
  COLPT cur_row;
public:
  PlainColumn(const DataType* ptr, const COLPT size)
    : ptr(ptr), size(size), cur_row(0)
  {};
  COLPT get_size() {return size;}
  DataType get(COLPT i) {return ptr[i];}
  DataType next() {;}
};

template <typename DataType>
class SortedPlainColumn : public PlainColumn<DataType>, public SortedColumn<DataType> {
private:
  const DataType* ptr;
  const COLPT size;
  COLPT cur_row;
public:
  SortedPlainColumn(const DataType* ptr, const COLPT size)
    : ptr(ptr), size(size), cur_row(0)
  {};
  COLPT get_size() {return size;}
  DataType get(COLPT i) {return ptr[i];}
  DataType next() {;}
};

#endif
