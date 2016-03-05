#! /usr/bin/python3

from nlp import NLP

string ="eid who works in dept id 5,4,3 and is a manager"

a = NLP(string)
a.replaceContractions()
a.tokenize()
a.removePunctAndStop()
a.replaceRelations()
a.replaceAttr()
a.reconstruct()
a.replaceOperators()
a.replaceSynAttr()
a.replaceSynCommon()
print (a.lowercase_query)
a.andOr()
a.unknownAttr()
a.relationSearch()
a.negationCheck()
print(a.SELECT)
print(a.FROM)
print (a.WHERE)

