#! /usr/bin/python3
import shelve

conf = shelve.open('conf')

print(conf['relations'])

print(conf['ant_operators'])
print(conf['replace_operators'])
print(conf['replace_contractions'])
