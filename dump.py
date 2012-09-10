#! /usr/bin/python
from yaml import load
from coldb import schema
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    with open('sample.yml', 'rb') as f:
        ymldata = f.read()
    config = load(ymldata)

    s = schema.Schema(config)
    with open('sampledata.yml', 'rb') as f:
        data = f.read()
    data = load(data)
    print len(s.make_data(data))

if __name__ == '__main__':
    main()
