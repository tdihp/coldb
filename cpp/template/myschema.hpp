#ifndef INCLUDED_MYSCHEMA_HPP
#define INCLUDED_MYSCHEMA_HPP

#include "coldb/types.hpp"
#include "coldb/column.hpp"
#include "coldb/factory.hpp"

namespace myschema
{
class Schema
{
public:
  {% for table in tables %}
    struct {{table.name}}
    {
      {{table.name}}(I32 data_size, void*& col_def, void*& col_ptr)
        : data_size_(data_size)
      {
        if(!data_size_) {return;}
        char data_type;
        char compress_id;
        {% for col_uniname in table.col_uninames %}
          {% set col = schema.col_by_uniname[col_uniname] %}
          data_type = *((char*)col_def++);
          compress_id = *((char*)col_def++);
          U32 col_size = *((U16*)col_def++);
          {% if col.fkey %}
            {% set tgttable = schema.table_by_name[col.fkey] %}
            {% set tgtcol = schema.col_by_uniname[tgttable.pkey] %}
            {% if col.pkey or col.skey %}
              // sorted fkey column
              {{col.name}} = i_sfcol_factory<{{DATATYPE2CTYPE[tgtcol.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_, {{tgttable.name}}_.{{tgtcol.name}});
            {% else %}
              // fkey column
              {{col.name}} = i_fcol_factory<{{DATATYPE2CTYPE[tgtcol.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_, {{tgttable.name}}_.{{tgtcol.name}});
            {% endif %}
          {% elif col.datatype in DATATYPE2CTYPE %}
            {% if col.pkey or col.skey %}
              // sorted column
              {{col.name}} = i_scol_factory<{{DATATYPE2CTYPE[tgtcol.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_);
            {% else %}
              // normal column
              {{col.name}} = i_col_factory<{{DATATYPE2CTYPE[tgtcol.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_);
            {% endif %}
          {% elif is_struct_datatype(col.datatype) %}
            {% set size = datatype2struct(col.datatype) %}
              // struct column
              {{col.name}} = s_col_factory<size>(data_type, compress_id, col_ptr, data_size_);
          {% else %}
            {% set align = datatype2blob(col.datatype) %}
              // blob column
              {{col.name}} = b_col_factory<align>(data_type, compress_id, col_ptr, data_size_);
          {% endif %}

          (U32*)col_ptr += col_size;
        {% endfor %}
      }
      
      I32 data_size_;
      // column members
      {% for col_uniname in table.col_uninames %}
        {% set col = schema.col_by_uniname[col_uniname] %}
        {% if col.fkey %}
          {% set tgttable = schema.table_by_name[col.fkey] %}
          {% set tgtcol = schema.col_by_uniname[tgttable.pkey] %}
          {% if col.pkey or col.skey %}
            // sorted fkey column
            SortedFKeyColumn<{{DATATYPE2CTYPE[tgtcol.datatype]}}>* {{col.name}} = 0;
          {% else %}
            // fkey column
            FKeyColumn<{{DATATYPE2CTYPE[tgtcol.datatype]}}>* {{col.name}} = 0;
          {% endif %}
        {% elif col.datatype in DATATYPE2CTYPE %}
          {% if col.pkey or col.skey %}
            // sorted column
            SortedColumn<{{DATATYPE2CTYPE[col.datatype]}}>* {{col.name}} = 0;
          {% else %}
            // normal column
            Column<{{DATATYPE2CTYPE[col.datatype]}}>* {{col.name}} = 0;
          {% endif %}
        {% elif is_struct_datatype(col.datatype) %}
          {% set size = datatype2struct(col.datatype) %}
            // struct column
            Column<std::string>* {{col.name}} = 0;
        {% else %}
          {% set align = datatype2blob(col.datatype) %}
            // blob column
            Column<std::string>* {{col.name}} = 0;
        {% endif %}
      {% endfor %}
    } {{table.name}}_;

  {% endfor %}


  Schema(void* buffer)
  {
    // skip magic word
    (U32*)buffer += 1;
    
    U16* table_sizes = buffer;
    void* col_def = aligned<U32>(buffer + {{tables|length}});
    // get first col_ptr by walk through each table
    U16* _tmp_table_sizes = table_sizes;
    void* col_ptr = col_def; // just initial value, use it to walk
    U32 table_size;
    {% for table in tables %}
      // {{table.name}}
      table_size = *(_tmp_table_sizes++);
      if(table_size)
      {
        (char*)col_ptr += 4 * {{table.col_uninames|length}};
      }
    {% endfor %}
    
    // initial each table
    _tmp_table_sizes = table_sizes;
    {% for table in tables %}
      // {{table.name}}
      table_size = *(_tmp_table_sizes++);
      {{table.name}}_ = {{table.name}}(table_size, col_def, col_ptr);
    {% endfor %}
  }

}

}

#endif
