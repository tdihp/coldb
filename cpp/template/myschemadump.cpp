#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

#include "myschema.hpp"

using namespace myschema;
using namespace std;

ifstream::pos_type size;
char * memblock;

string write_escaped(string const& s)
{
  ostringstream out(ostringstream::out);
  out << '"';
  for (string::const_iterator i = s.begin(), end = s.end(); i != end; ++i) {
    unsigned char c = *i;
    if (' ' <= c and c <= '~' and c != '\\' and c != '"') {
      out << c;
    }
    else {
      out << '\\';
      switch(c) {
      case '"':  out << '"';  break;
      case '\\': out << '\\'; break;
      case '\t': out << 't';  break;
      case '\r': out << 'r';  break;
      case '\n': out << 'n';  break;
      default:
        char const* const hexdig = "0123456789ABCDEF";
        out << 'x';
        out << hexdig[c >> 4];
        out << hexdig[c & 0xF];
      }
    }
  }
  out << '"';
  return out.str();
}

int dump_file(char* fname) {
  ifstream file (fname, ios::in|ios::binary|ios::ate);
  if (file.is_open())
  {
	cout << "dumping " << fname << endl;
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
      << write_escaped(schema.{{table.name}}_.{{col.name}}->get(i)) << ", "
      {%   endif -%}
      {% endfor -%}
      << endl;
    }
    {% endfor -%}

    delete[] memblock;
  }
  else cout << "Unable to open file " << fname << endl ;
}

int main(int argc, char* argv[]) {
  if (argc > 1){
    for(int i = 1; i < argc; ++i) {
    	dump_file(argv[i]);
    }
  }
  return 0;
}
