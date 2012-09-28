#! /usr/bin/python
import logging

from yaml import load
import jinja2

from coldb import schema

def main():
    logging.basicConfig(level=logging.INFO)
    with open('sample.yml', 'rb') as f:
        ymldata = f.read()
    config = load(ymldata)

    s = schema.Schema(config)
    with open('sampledata.yml', 'rb') as f:
        data = f.read()
    data = load(data)

    with open('sampledata.dat', 'wb') as f:
        f.write(s.make_data(data))

    with open('./cpp/template/myschema.hpp', 'rb') as f:
        hpptemplate = f.read()

    with open('./cpp/template/myschemadump.cpp', 'rb') as f:
        dumptemplate = f.read()

    from coldb.common import *

    with open('./myschema.hpp', 'wb') as f:
        f.write(jinja2.Template(hpptemplate).render(schema=s, tables=s._tables, **locals()))

    with open('./myschemadump.cpp', 'wb') as f:
        f.write(jinja2.Template(dumptemplate).render(schema=s, tables=s._tables, **locals()))

if __name__ == '__main__':
    main()
