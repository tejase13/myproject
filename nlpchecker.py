#! /usr/bin/python3

from nlp import NLP

string = "employee name with dept id not greater than 5 and dept id not less than 1"

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
a.constantAssociation()
a.commonAssociation()
a.unknownAttr()
a.relationSearch()
a.negationCheck()
print(a.SELECT)
print(a.FROM)
print (a.WHERE)

