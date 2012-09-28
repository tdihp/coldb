#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

#include "myschema.hpp"

using namespace myschema;
using namespace std;

ifstream::pos_type size;
char * memblock;

string bin2hex(string instr)
{
  ostringstream oss (ostringstream::out);
  for(int i = 0; i < instr.size(); ++i)
  {
    oss << setw(2) << setfill('0') << hex << (unsigned int)(instr.data()[i]);
  }
  return oss.str();
}

int main() {
  ifstream file ("example.dat", ios::in|ios::binary|ios::ate);
  if (file.is_open())
  {
    size = file.tellg();
    memblock = new char [size];
    file.seekg (0, ios::beg);
    file.read (memblock, size);
    file.close();
    myschema::Schema schema((void*)memblock);

    {% for table in tables -%}
    cout << "{{table.name}}: " << schema.{{table.name}}_.data_size_ << endl;
    for(int i = 0; i < schema.{{table.name}}_.data_size_; ++i)
    {
      cout
      {% for col_uniname in table.col_uninames -%}
      {% set col = schema.col_by_uniname[col_uniname] -%}
      {%   if not (is_struct_datatype(col.datatype) or is_blob_datatype(col.datatype)) -%}
      {%     if col.datatype in ('b', 'B') -%}
      << int(schema.{{table.name}}_.{{col.name}}->get(i)) << ", "
      {%     else -%}
      << schema.{{table.name}}_.{{col.name}}->get(i) << ", "
      {%     endif -%}
      {%   else -%}
      << bin2hex(schema.{{table.name}}_.{{col.name}}->get(i)) << ", "
      {%   endif -%}
      {% endfor -%}
      << endl;
    }
    {% endfor -%}
    
    delete[] memblock;
  }
  else cout << "Unable to open file";
  return 0;
}
