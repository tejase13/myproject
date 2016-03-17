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
		self.syn_aggregate = conf['syn_aggregate']
		self.aggregate_list = conf['aggregate_list']

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
		keyword_copy = list(keywords)
		length = len(keywords)
		for index in range(length):
			if keywords[index] in entity:
				keyword_copy[index] = entity[keywords[index]]
		return keyword_copy

	def replaceRelations(self):
		self.keyword_copy = self.replaceKeywordsWithEntity (self.keywords, self.relations)

	def replaceAttr(self):
		self.keyword_copy = self.replaceKeywordsWithEntity (self.keyword_copy, self.replace_attr)
	
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

  	#Find all constants between self.start_index and self.end_index
	def constantAssociation(self, start_index, end_index):
		self.SELECT = []
		#self.WHERE= {}
		self.FROM = {}
		#self.constant_assoc = self.lowercase_query.split(' ')
		print(start_index)
		print(end_index)

		#temp_list stores all where clause elements in the form attr,operator,constant
		temp_list = []

		#counter is used to shift the end_index due to removal of operators and constants
		#stores number of elements removed in each iteration
		counter = 0
		self.default_operator = "="

		while True:
			match = False
			for i in range(start_index,end_index):
				#if constant is found
				if self.constant_assoc[i].isdigit():
					j = i 
					match = True
					while j >= start_index:
						#if attribute is found
						if self.constant_assoc[j] in self.attr_relations:
							#search for operator between the position of attribute and constant
							operator = self.operatorSearch(j,i)
							#Appending to unique or common attribute relation list
							rel = self.attr_relations[self.constant_assoc[j]]
							if len(rel) == 1:
								if rel[0] not in self.unique_attribute_relation:
									self.unique_attribute_relation.append(rel[0])
							else:
								for element in rel:						
									if  element not in self.common_attribute_relation:
										self.common_attribute_relation.append(element)

							if operator is None: #use default operator
								self.assignConstant(temp_list, self.constant_assoc[j], self.default_operator, self.constant_assoc[i])
								print (temp_list)
								self.constant_assoc.remove(self.constant_assoc[i])
								counter += 1

							else:
								self.assignConstant(temp_list, self.constant_assoc[j], self.constant_assoc[operator], self.constant_assoc[i])
								self.default_operator = self.constant_assoc[operator] 
								self.constant_assoc.remove(self.constant_assoc[i])
								self.constant_assoc.remove(self.constant_assoc[operator])
								counter += 2
							break
						j = j - 1

					#if no attribute found
					if j < start_index:
						operator = self.operatorSearch(start_index,i)
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

			end_index = end_index - counter
			counter = 0

		print(temp_list)

		#return new end_index and the list with all the elements
		return [end_index, temp_list]	

	
	def commonAssociation(self, start_index, end_index):
		print(start_index)
		print(end_index)
		self.lowercase_query = ' '.join(self.constant_assoc[start_index : end_index])
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
					#Appending to unique or common attribute relation list
					rel = self.attr_relations[self.common_attr[key]]
					if len(rel) == 1:
						if rel[0] not in self.unique_attribute_relation:
							self.unique_attribute_relation.append(rel[0])
					else:
						for element in rel:
							if  element not in self.common_attribute_relation:
								self.common_attribute_relation.append(element)
					

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
	def assignEntity (self):
		print(self.where_elements)
		while len(self.where_elements) > 0:
			if self.where_elementsIndex % 3 == 0:
				if not self.isAttr(self.where_elements[self.where_elementsIndex]):
					self.where_elements.insert(self.where_elementsIndex,self.default_attribute)
				self.where_list.append(self.where_elements[self.where_elementsIndex])

			if self.where_elementsIndex % 3 == 1:
				if not self.isOper(self.where_elements[self.where_elementsIndex]):
					self.where_elements.insert(self.where_elementsIndex,self.default_operator)
				self.where_list.append(self.where_elements[self.where_elementsIndex])

			if self.where_elementsIndex % 3 == 2:
				self.where_list.append(self.where_elements[self.where_elementsIndex])
				if self.end_index < len(self.constant_assoc):
					self.where_list.append(self.constant_assoc[self.end_index])
				else:
					self.where_list.append(self.default_logical_operator)
			self.where_elementsIndex += 1

			if self.where_elementsIndex >= len(self.where_elements):
				break

	def andOr(self):
		self.constant_assoc = self.lowercase_query.split(' ')
		print(self.constant_assoc)

		#a list with all elements of where clause along with their and/or conjunctions
		self.where_list = []
		self.start_index = -1 
		self.end_index = 0
		self.default_operator = ""
		self.default_attribute = ""
		self.default_logical_operator = "and"
		#Stores relations with unique attr in one list and relations with common attr in the other
		self.unique_attribute_relation = []
		self.common_attribute_relation = []

		#searches for and/or and finds constants and attributes before them
		while True:
			if self.constant_assoc[self.end_index] == "and" or self.constant_assoc[self.end_index] == "or":
				self.default_logical_operator = self.constant_assoc[self.end_index]
				self.returned_list = self.constantAssociation(self.start_index + 1,self.end_index)

				self.where_elements = self.returned_list[1]
				self.end_index = self.returned_list[0]
				self.where_elementsIndex = 0

				#traverse through the returned list and append attributes and operators in the list
				#if they are not present for a particular constant
				self.assignEntity ()

				# in case there is no constant present between self.start_index and self.end_index we won't be able to get
				# a default attribute and default operator from the self.where_list		
				if len(self.where_list) > 0:
					self.default_attribute = self.where_list[-4]
					self.default_operator = self.where_list[-3]
				# We're checking for common associations and appending the returned list to self.where_list
				#self.where_common_list = []
				self.returned_common_list = self.commonAssociation(self.start_index + 1, self.end_index)
				#Traverse through the list and add default logical operator
				for i in range(len(self.returned_common_list)):
					if i % 3 == 2:
						self.where_list.append(self.returned_common_list[i])
						self.where_list.append(self.default_logical_operator)
					else:
						self.where_list.append(self.returned_common_list[i])						 
				self.start_index = self.end_index


			self.end_index += 1
			if self.end_index >= len(self.constant_assoc):
					break

		#search again when the end of list is reached
		self.returned_list = self.constantAssociation(self.start_index + 1,self.end_index)
		self.where_elements = self.returned_list[1]
		self.end_index = self.returned_list[0]

		self.where_elementsIndex = 0
		self.assignEntity ()

		# We're checking for common associations and appending the returned list to self.where_list
		self.where_common_list = []
		print('hi')
		self.returned_common_list = self.commonAssociation(self.start_index + 1, self.end_index)
		#Traverse through the list and add default logical operator
		for i in range(len(self.returned_common_list)):
			if i % 3 == 2:
				self.where_list.append(self.returned_common_list[i])
				self.where_list.append(self.default_logical_operator)
			else:
				self.where_list.append(self.returned_common_list[i])						 
		self.start_index = self.end_index
		if len(self.where_list) > 0:
			self.where_list.pop()
		print (self.where_list)	

	
	def backwardSearch(self, start_index, end_index):
		index = end_index - 1
		s = self.constant_assoc[end_index]
		match = False	
		while index >= start_index:
			if self.constant_assoc[index] in self.operator_list:
				print(self.constant_assoc[index])
				i = index - 1
				print(i)
				while i >= start_index:
					if self.isAttr(self.constant_assoc[i]):
						#Appending to unique or common attribute relation list
						rel = self.attr_relations[self.constant_assoc[i]]
						if len(rel) == 1:
							if rel[0] not in self.unique_attribute_relation:
								self.unique_attribute_relation.append(rel[0])
						else:
							for element in rel:
								if  element not in self.common_attribute_relation:
									self.common_attribute_relation.append(element)
						#Stores index for removal of aggr attribute
						if i not in self.remove_list:
							self.remove_list.append(i)
						s = s + '(' + self.constant_assoc[i] + ')'
						rel = self.attr_relations[self.constant_assoc[i]] 
						for j in rel:
							if j in self.FROM:
								self.FROM[j] += 1
							else:
								self.FROM[j] = 1
						match = True
						break
					i = i - 1

			if match is True:
				break
			index = index - 1
		print(s)
		if match is True:
			self.SELECT.append(s)
		return match

	def forwardSearch(self, start_index, end_index):
		print('hi')
		s = self.constant_assoc[start_index]
		for index in range(start_index + 1, end_index):
			if self.isAttr(self.constant_assoc[index]):
				#Appending to unique or common attribute relation list
				rel = self.attr_relations[self.constant_assoc[index]]
				if len(rel) == 1:
					if rel[0] not in self.unique_attribute_relation:
						self.unique_attribute_relation.append(rel[0])
				else:
					for element in rel:
						if  element not in self.common_attribute_relation:
							self.common_attribute_relation.append(element)
				
				if index not in self.remove_list:
					self.remove_list.append(index)
				s = s + '(' + self.constant_assoc[index] + ')'
				rel = self.attr_relations[self.constant_assoc[index]]
				for i in rel:
					if i in self.FROM:
						self.FROM[i] += 1
					else:
						self.FROM[i] = 1
				break
		self.SELECT.append(s)

	def unknownAttr(self):
		#self.constant_assoc = self.lowercase_query.split(' ')
		print("Unknown attr ",self.constant_assoc)
		lowercase_query = ' ' .join(self.constant_assoc)
		lowercase_query = self.replaceQueryTermWithEntity(lowercase_query, self.syn_aggregate)
		self.constant_assoc = lowercase_query.split(' ')
		self.remove_list = []
		start_index = 0
		end_index = 0
		for index in range(len(self.constant_assoc)):
			if self.constant_assoc[index] in self.aggregate_list and self.constant_assoc[index] != 'count':
				end_index = index
				result = self.backwardSearch(start_index, end_index)
				print(result)
				if result:
					start_index = end_index + 1
					continue

				else:
					self.forwardSearch(end_index, len(self.constant_assoc)) 
					start_index = end_index + 1

			elif self.constant_assoc[index] == 'count':
				str = 'count(*)'
				self.SELECT.append(str)
				start_index = index + 1
		
		
		self.remove_list.sort()
		index = len(self.remove_list) - 1
		while index >= 0:
			self.constant_assoc.pop(self.remove_list[index])	
			index = index - 1

		# Non aggregate attributes
		print(self.constant_assoc)
		for index in self.constant_assoc:
			if self.isAttr(index):
				#Appending to unique or common attribute relation list
				rel = self.attr_relations[index]
				if len(rel) == 1:
					if rel[0] not in self.unique_attribute_relation:
						self.unique_attribute_relation.append(rel[0])
				else:
					for element in rel:
						if  element not in self.common_attribute_relation:
							self.common_attribute_relation.append(element)
				if index not in self.SELECT:
					self.SELECT.append(index)
				rel = self.attr_relations[index]
				for i in rel:
					if i in self.FROM:
						self.FROM[i] += 1
					else:
						self.FROM[i] = 1
		print("Select list:",self.SELECT)


	#searching the remaining keywords for relations
	def relationSearch(self):
		for index in self.constant_assoc:
			if index in self.relations:
				if index not in self.unique_attribute_relation:
					self.unique_attribute_relation.append(index)
		print ("Unique relation",self.unique_attribute_relation)
		print ("Common relation",self.common_attribute_relation)
					

	def negationCheck(self):
		bool = False
		for index in self.constant_assoc:
			if index == 'not': 
				bool = True
				break
		if bool and len(self.where_list) > 0:
			for index in range(len(self.where_list)):
				if (index + 1) % 4 == 2:
					self.where_list[index] = self.ant_operators[self.where_list[index]]
		
