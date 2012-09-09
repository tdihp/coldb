#! /usr/bin/python
from yaml import load
from coldb import schema

def main():

    with open('sample.yml', 'rb') as f:
        ymldata = f.read()
    config = load(ymldata)
    schema.Schema(config)
    print schema

if __name__ == '__main__':
    main()
