#! /usr/bin/python3

from nlp import NLP

string = "employee with dept id 10 emp id 3"

a = NLP(string)

a.tokenize()
a.removePunctAndStop()
a.replaceRelations()
a.replaceAttr()
a.reconstruct()
a.replaceSynAttr()
a.constantAssociation()
a.unknownAttr()

print (a.SELECT)
print (a.FROM)
print (a.WHERE)
