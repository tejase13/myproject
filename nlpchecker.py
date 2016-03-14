#! /usr/bin/python3

from nlp import NLP
from queryconstruction import QueryConstruction
string ="find the empname whose salary is maximum and also avg salary of all employees"

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
print(a.where_list)

b = QueryConstruction(a.SELECT, a.FROM, a.where_list)

b.constructSelectPart()
b.constructFromPart()
b.constructWherePart()

print(b.final_query)
