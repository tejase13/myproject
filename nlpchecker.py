#! /usr/bin/python3

from nlp import NLP
from queryconstruction import QueryConstruction
queries = open("testing.txt").readlines()
output = open('output.txt', 'w')
for string in queries:
#string ="Biggest and smallest project in terms of workforce"

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
        #print("Unique relation ",a.unique_attribute_relation)
        #print("Common relation ",a.common_attribute_relation)
	b = QueryConstruction(a.SELECT, a.FROM, a.where_list, a.unique_attribute_relation)

	b.checkJoin()
	b.constructSelectPart()
	b.constructFromPart()
	b.constructWherePart()

	print(b.final_query)
	output.write(b.final_query + '\n')
output.close()
