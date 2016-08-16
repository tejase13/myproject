#! /usr/bin/python3

from nlp import NLP
from queryconstruction import QueryConstruction
class NLPChecker():
	
#for string in queries:
#string ="Biggest and smallest project in terms of workforce"
	def execute(self, string):
		#print(queries.index(string))
		a = NLP(string)
		a.namedEntityRecognition()
		a.replaceContractions()
		a.lemmatize()

		print("Lemmatized query:", a.lowercase_query)
		a.tokenize()
		a.removePunctAndStop()
		a.replaceRelations()
		a.replaceAttr()
		a.reconstruct()
		a.replaceOperators()
		a.replaceSynAttr()
		a.replaceSynCommon()
		#print (a.lowercase_query)
		a.andOr()
		a.unknownAttr()
		a.relationSearch()
		a.negationCheck()
		a.removeDuplicates()
		a.cleaningSelectList()
		#print(a.SELECT)
		#print(a.WHERE)
		#print("Unique relation ",a.unique_attribute_relation)
		#print("Common relation ",a.common_attribute_relation)
		b = QueryConstruction(a.SELECT, a.WHERE, a.unique_attribute_relation, a.common_attribute_relation)

		b.checkJoin()
		b.constructSelectPart()
		check = b.constructFromPart()
		if check is True:
			b.constructWherePart()

		#print(b.final_query)
		return b.final_query


if __name__ == "__main__":
	l = NLPChecker()

	queries = open("testing.txt").readlines()
	output = open('output.txt', 'w')

	for string in queries:
		q = l.execute(string)
		
		output.write(q + '\n')
	output.close()
		


