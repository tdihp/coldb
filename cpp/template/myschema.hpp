#ifndef INCLUDED_MYSCHEMA_HPP
#define INCLUDED_MYSCHEMA_HPP

#include "coldb/types.hpp"
#include "coldb/column.hpp"
#include "coldb/factory.hpp"

namespace myschema
{
using namespace coldb;
class Schema
{
public:
  {% for table in tables %}
    struct {{table.name}}
    {
      I32 data_size_;
      // column members
      {% for col_uniname in table.col_uninames -%}
      {%   set col = schema.col_by_uniname[col_uniname] -%}
      {%   if col.fkey -%}
      {%     set tgttable = schema.table_by_name[col.fkey] -%}
      {%     set tgtcol = schema.col_by_uniname[tgttable.pkey] -%}
      {%     if col.pkey or col.skey -%}
      // sorted fkey column
      SortedFKeyColumn<{{DATATYPE2CTYPE[tgtcol.datatype]}}>* {{col.name}};
      {%     else -%}
      // fkey column
      FKeyColumn<{{DATATYPE2CTYPE[tgtcol.datatype]}}>* {{col.name}};
      {%     endif -%}
      {%   elif col.datatype in DATATYPE2CTYPE -%}
      {%     if col.pkey or col.skey -%}
      // sorted column
      SortedColumn<{{DATATYPE2CTYPE[col.datatype]}}>* {{col.name}};
      {%     else -%}
      // normal column
      Column<{{DATATYPE2CTYPE[col.datatype]}}>* {{col.name}};
      {%     endif -%}
      {%   elif is_struct_datatype(col.datatype) -%}
      {%     set size = datatype2struct(col.datatype) -%}
      // struct column
      Column<std::string>* {{col.name}};
      {%   else -%}
      {%     set align = datatype2blob(col.datatype) -%}
      // blob column
      Column<std::string>* {{col.name}};
      {%   endif -%}
      {% endfor %}

      {{table.name}}()
        : data_size_(0),
      {% for col_uniname in table.col_uninames -%}
        {% set col = schema.col_by_uniname[col_uniname] -%}
        {% if loop.last -%}
        {{col.name}}(0)
        {% else -%}
        {{col.name}}(0),
        {% endif -%}
      {% endfor -%}
      {}

      void init(Schema* cur_schema, I32 data_size, void*& col_def, void*& col_ptr)
      {
        data_size_ = data_size;
        if(!data_size_) {return;}
        char data_type;
        char compress_id;
        U32 col_size;
        {% for col_uniname in table.col_uninames -%}
        {%   set col = schema.col_by_uniname[col_uniname] -%}
        // {{col.name}}
        data_type = *((char*)col_def);
        col_def = (char*)col_def + 1;
        compress_id = *((char*)col_def);
        col_def = (char*)col_def + 1;
        {%   if col.fkey -%}
        {%     set tgttable = schema.table_by_name[col.fkey] -%}
        {%     set tgtcol = schema.col_by_uniname[tgttable.pkey] -%}
        {%     if col.pkey or col.skey -%}
        // sorted fkey column
        {{col.name}} = i_sfcol_factory<{{DATATYPE2CTYPE[tgtcol.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_, cur_schema->{{tgttable.name}}_.{{tgtcol.name}});
        {%     else -%}
        // fkey column
        {{col.name}} = i_fcol_factory<{{DATATYPE2CTYPE[tgtcol.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_, cur_schema->{{tgttable.name}}_.{{tgtcol.name}});
        {%     endif -%}
        {%   elif col.datatype in DATATYPE2CTYPE -%}
        {%     if col.pkey or col.skey -%}
        // sorted column
        {{col.name}} = i_scol_factory<{{DATATYPE2CTYPE[col.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_);
        {%     else -%}
        // normal column
        {{col.name}} = i_col_factory<{{DATATYPE2CTYPE[col.datatype]}}, U16, U8>(data_type, compress_id, col_ptr, data_size_);
        {%     endif -%}
        {%   elif is_struct_datatype(col.datatype) -%}
        {%     set size = datatype2struct(col.datatype) -%}
        // struct column
        {{col.name}} = s_col_factory<{{size}}>(data_type, compress_id, col_ptr, data_size_);
        {%   else -%}
        {%     set align = datatype2blob(col.datatype) -%}
        // blob column
        {{col.name}} = b_col_factory<U16, {{align}}>(data_type, compress_id, col_ptr, data_size_);
        {%   endif -%}
        {% endfor %}
      }

      ~{{table.name}}()
      {
        {% for col_uniname in table.col_uninames -%}
        {%   set col = schema.col_by_uniname[col_uniname] -%}
        if({{col.name}})
        {
          delete {{col.name}};
          {{col.name}} = 0;
        }
        {% endfor -%}
      }
    } {{table.name}}_;

  {% endfor -%}


  Schema(void* buffer)
  {
    // skip magic word
    buffer = (U32*)buffer + 1;

    U16* table_sizes = (U16*)buffer;
    void* col_def = aligned<sizeof(ALIGN_T)>(table_sizes + {{tables|length}});
    // get first col_ptr by walk through each table
    U16* _tmp_table_sizes = table_sizes;
    void* col_ptr = col_def; // just initial value, use it to walk
    U32 table_size;
    {% for table in tables -%}
    // {{table.name}}
    table_size = *(_tmp_table_sizes++);
    if(table_size)
    {
      col_ptr = (char*)col_ptr + 4 * {{table.col_uninames|length}};
    }
    {% endfor -%}

    // initial each table
    _tmp_table_sizes = table_sizes;
    {% for table in tables -%}
    // {{table.name}}
    table_size = *(_tmp_table_sizes++);
    {{table.name}}_.init(this, table_size, col_def, col_ptr);
    {% endfor %}
  }

};

}

#endif
