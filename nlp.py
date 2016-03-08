#! /usr/bin/python3

import string
import shelve,time
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordPunctTokenizer

class NLP:
	def __init__ (self, query):
		#Importing all dicts from conf file 
		conf = shelve.open('conf')
		self.relations = conf['relations']
		self.attr_relations = conf['attr_relations']
		self.replace_attr = conf['replace_attr']
		self.syn_attr = conf['syn_attr']
		self.syn_common = conf['syn_common']
		self.common_attr = conf['common_attr']
		self.relations_attr = conf['relations_attr']
		self.replace_contractions = conf['replace_contractions']	
		self.replace_operators = conf['replace_operators']
		self.operator_list = conf['operator_list']
		self.ant_operators = conf['ant_operators']

		#Original Query	
		self.original_query = query
		self.lowercase_query = self.original_query.lower()

		#Stop words list
		self.stop_words = list(stopwords.words("english"))
		self.stop_words.remove('of')
		self.stop_words.remove('not')
		self.stop_words.remove('is')
		self.stop_words.remove('nor')
		self.stop_words.remove('and')
		self.stop_words.remove('or')
		self.stop_words.remove('but')
		self.stop_words.remove('did')
		self.stop_words.append('whose')
		self.stop_words.append('tell')
		self.stop_words.append('give')
		self.stop_words.append('display')
		self.stop_words.append('list')
		self.stop_words.append('print')
		self.stop_words.append('show')
		self.stop_words.append('select')
		self.stop_words.append('fetch')
		self.stop_words.append('search')
		self.stop_words.append('get')
		self.stop_words.append('want')


	def replaceContractions(self):
		for key in self.replace_contractions:
			if self.lowercase_query.find(key) != -1:
				self.lowercase_query = self.lowercase_query.replace(key, self.replace_contractions[key])

	def tokenize(self):
		self.words = WordPunctTokenizer().tokenize(self.lowercase_query)
		self.punct_list = list(string.punctuation)
		self.punct_list.remove('<')
		self.punct_list.remove('>')
		self.punct_list.remove('!')
		self.punct_list.remove('=')
		self.punct_list.remove('*')
		self.punct_list.remove('/')
		self.alpha_list = list(string.ascii_lowercase)

	def removePunctAndStop(self):
		self.keywords = []
		for word in self.words:
			if word not in self.punct_list and word not in self.alpha_list and word not in self.stop_words:
				self.keywords.append(word)

	def replaceKeywordsWithEntity(self, keywords, entity):
		self.keyword_copy = list(keywords)
		length = len(keywords)
		for index in range(length):
			if keywords[index] in entity:
				self.keyword_copy[index] = entity[keywords[index]]
		return self.keyword_copy

	def replaceRelations(self):
		self.keyword_copy = self.replaceKeywordsWithEntity (self.keywords, self.relations)
	
	def replaceAttr(self):
		self.keyword_copy = self.replaceKeywordsWithEntity (self.keywords, self.replace_attr)

	def reconstruct(self):
		self.lowercase_query = ' '.join(self.keyword_copy)

	def replaceQueryTermWithEntity (self, query, entity):
		for key in entity:
			if query.find(key) != -1:
				query = query.replace(key, entity[key])
		return query

	def replaceOperators(self):
		self.lowercase_query = self.replaceQueryTermWithEntity (self.lowercase_query, self.replace_operators)

	def replaceSynAttr(self):
		self.lowercase_query = self.replaceQueryTermWithEntity (self.lowercase_query, self.syn_attr)
	
	def replaceSynCommon(self):
		self.lowercase_query = self.replaceQueryTermWithEntity (self.lowercase_query, self.syn_common)
	
	def operatorSearch(self, j, i):
		for index in range(j,i):
			if self.constant_assoc[index] in self.operator_list:
				return index
		return None

	def assignConstant (self, list, a, b, c):
		list.append(a)
		list.append(b)
		list.append(c)

  	#Find all constants between startIndex and endIndex
	def constantAssociation(self, startIndex, endIndex):
		#self.SELECT = []
		#self.WHERE= {}
		#self.FROM = {}
		#self.constant_assoc = self.lowercase_query.split(' ')
		print(startIndex)
		print(endIndex)

		#temp_list stores all where clause elements in the form attr,operator,constant
		temp_list = []

		#counter is used to shift the endIndex due to removal of operators and constants
		#stores number of elements removed in each iteration
		counter = 0
		defaultOperator = "="

		while True:
			match = False
			for i in range(startIndex,endIndex):
				#if constant is found
				if self.constant_assoc[i].isdigit():
					j = i 
					match = True
					while j >= startIndex:
						#if attribute is found
						if self.constant_assoc[j] in self.attr_relations:
							#search for operator between the position of attribute and constant
							operator = self.operatorSearch(j,i)

							if operator is None: #use default operator
								self.assignConstant(temp_list, self.constant_assoc[j], defaultOperator, self.constant_assoc[i])
								print (temp_list)
								self.constant_assoc.remove(self.constant_assoc[i])
								counter += 1

							else:
								self.assignConstant(temp_list, self.constant_assoc[j], self.constant_assoc[operator], self.constant_assoc[i])
								defaultOperator = self.constant_assoc[operator] 
								self.constant_assoc.remove(self.constant_assoc[i])
								self.constant_assoc.remove(self.constant_assoc[operator])
								counter += 2
							break
						j = j - 1

					#if no attribute found
					if j < startIndex:
						operator = self.operatorSearch(startIndex,i)
						if operator is not None:
							temp_list.append(self.constant_assoc[operator])
							counter += 1
						temp_list.append(self.constant_assoc[i])
						self.constant_assoc.remove(self.constant_assoc[i])
						if operator is not None:
							self.constant_assoc.remove(self.constant_assoc[operator])
						counter += 1
					break

			#when no constant found break
			if match is False:
				break

			endIndex = endIndex - counter
			counter = 0

		print(temp_list)

		#return new endIndex and the list with all the elements
		return [endIndex, temp_list]	

	
	def commonAssociation(self, startIndex, endIndex):
		print(startIndex)
		print(endIndex)
		self.lowercase_query = ' '.join(self.constant_assoc[startIndex : endIndex])
		print(self.lowercase_query)
		temp_list = []
		while True:
			match = False
			for key in self.common_attr:
				if self.lowercase_query.find(key) != -1:
					match = True
					# similar implementation to the above method dealing with duplicates in FROM dictionary
					self.assignConstant(temp_list, self.common_attr[key], '=', key)
					self.lowercase_query = self.lowercase_query.replace(key, '')

			if match is False:
				break
		return temp_list


	def isAttr(self, var):
		if var in self.attr_relations:
			return True
		return False

	def isOper(self, var):
		if var in self.operator_list:
			return True
		return False

	#traverse through the returned list and append attributes and operators in the list
	#if they are not present for a particular constant
	def assignEntity (self, whereList, whereElements, whereElementsIndex, defaultAttribute, defaultOperator, endIndex):
		while len(whereElements) > 0:
				if whereElementsIndex % 3 == 0:
					if not self.isAttr(whereElements[whereElementsIndex]):
							whereElements.insert(whereElementsIndex,defaultAttribute)
						whereList.append(whereElements[whereElementsIndex])

					if whereElementsIndex % 3 == 1:
						if not self.isOper(whereElements[whereElementsIndex]):
							whereElements.insert(whereElementsIndex,defaultOperator)
						whereList.append(whereElements[whereElementsIndex])

					if whereElementsIndex % 3 == 2:
						whereList.append(whereElements[whereElementsIndex])
						whereList.append(self.constant_assoc[endIndex])
					whereElementsIndex += 1

					if whereElementsIndex >= len(whereElements):
						break

	def andOr(self):
		self.constant_assoc = self.lowercase_query.split(' ')
		print(self.constant_assoc)

		#a list with all elements of where clause along with their and/or conjunctions
		whereList = []
		startIndex = -1 
		endIndex = 0
		defaultOperator = ""
		defaultAttribute = ""
		defaultLogicalOperator = "and"

		#searches for and/or and finds constants and attributes before them
		while True:
			if self.constant_assoc[endIndex] == "and" or self.constant_assoc[endIndex] == "or":
				defaultLogicalOperator = self.constant_assoc[endIndex]
				returnedList = self.constantAssociation(startIndex + 1,endIndex)

				whereElements = returnedList[1]
				endIndex = returnedList[0]
				whereElementsIndex = 0

				#traverse through the returned list and append attributes and operators in the list
				#if they are not present for a particular constant
				self.assignEntity (whereList, whereElements, whereElementsIndex, defaultAttribute, defaultOperator, endIndex)

				# in case there is no constant present between startIndex and endIndex we won't be able to get
				# a default attribute and default operator from the whereList		
				if len(whereList) > 0:
					defaultAttribute = whereList[-4]
					defaultOperator = whereList[-3]
				# We're checking for common associations and appending the returned list to whereList
				#whereCommonList = []
				returnedCommonList = self.commonAssociation(startIndex + 1, endIndex)
				#Traverse through the list and add default logical operator
				for i in range(len(returnedCommonList)):
					if i % 3 == 2:
						whereList.append(returnedCommonList[i])
						whereList.append(defaultLogicalOperator)
					else:
						whereList.append(returnedCommonList[i])						 
				startIndex = endIndex


			endIndex += 1
			if endIndex >= len(self.constant_assoc):
					break

		#search again when the end of list is reached
		returnedList = self.constantAssociation(startIndex + 1,endIndex)
		whereElements = returnedList[1]
		endIndex = returnedList[0]

		whereElementsIndex = 0
		self.assignEntity (whereList, whereElements, whereElementsIndex, defaultAttribute, defaultOperator, endIndex)

		# We're checking for common associations and appending the returned list to whereList
		whereCommonList = []
		print('hi')
		returnedCommonList = self.commonAssociation(startIndex + 1, endIndex)
		#Traverse through the list and add default logical operator
		for i in range(len(returnedCommonList)):
			if i % 3 == 2:
				whereList.append(returnedCommonList[i])
				whereList.append(defaultLogicalOperator)
			else:
				whereList.append(returnedCommonList[i])						 
		startIndex = endIndex
		if len(whereList) > 0:
			whereList.pop()
		print (whereList)	
							


	def unknownAttr(self):
		self.constant_assoc = self.lowercase_query.split(' ')
		for index in self.constant_assoc:
			if index in self.attr_relations:
				rel = self.attr_relations[index]
				for value in rel:
					if value in self.FROM:
						self.FROM[value] += 1
					else:
						self.FROM[value] = 1
				if index not in self.SELECT: # if unknown attribute does not already exist in select list then append
					self.SELECT.append(index)


	#searching the remaining keywords for relations
	def relationSearch(self):
		for index in self.constant_assoc:
			if index in self.relations:
				if index in self.FROM:
					self.FROM[index] += 1
				else:
					self.FROM[index] = 1
					

	def negationCheck(self):
		bool = False
		for index in self.constant_assoc:
			if index == 'not':
				bool = True
				break
		if bool:
			for key in self.WHERE:
				val_list = self.WHERE[key]
				index = 0
				while index < len(val_list):
					val_list[index] = self.ant_operators[val_list[index]]
					index += 2
