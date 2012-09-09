#! /usr/bin/python
from yaml import load
from coldb import schema

def main():

    with open('sample.yml', 'rb') as f:
        ymldata = f.read()
    config = load(ymldata)

    print schema.Schema(config)

if __name__ == '__main__':
    main()
