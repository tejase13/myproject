#! /usr/bin/python3
import shelve

conf = shelve.open('conf')

print(conf['relations'])

print(conf['replace_operators'])
