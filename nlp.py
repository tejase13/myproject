#! /usr/bin/python3

import string
import shelve,time
import re 
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordPunctTokenizer
from initialization import Initialization
from ner import NER
from lemma import Lemma
from nltk.stem import WordNetLemmatizer


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
		self.proper_nouns = conf['proper_nouns']

		#Original Query	
		self.original_query = query
		self.lowercase_query = self.original_query.lower()

		#Stop words list
		init = Initialization()
		self.stop_words = init.initializeStopWords()

	def namedEntityRecognition(self):
		ne = NER(self.original_query)
		self.entities = ne.performNER()
		self.named_entities = [ne.lower() for ne in self.entities]
		#print (self.named_entities)

	#Replace all contractions like isn't with is not and some other substitutions
	def replaceContractions(self):
		for contraction in self.replace_contractions:
			regex = '\\b' + contraction + '\\b'
			self.lowercase_query = re.sub(regex, self.replace_contractions[contraction], self.lowercase_query)

	def lemmatize(self):
		lem = Lemma()
		self.lowercase_query = lem.queryLemmatize(self.lowercase_query)

	
	#Break into tokens and initialize punctuation and alphabet lists
	def tokenize(self):
		self.words = WordPunctTokenizer().tokenize(self.lowercase_query)
		init = Initialization()
		self.punct_list = init.initializePunctList()
		self.alpha_list = list(string.ascii_lowercase)

	#Remove stop words and punctuations and individual alphabets
	def removePunctAndStop(self):
		self.keywords = [word for word in self.words if word not in self.punct_list and word not in self.alpha_list and word not in self.stop_words]

	#Method used for substituting individual tokens with their domain relevant words
	def replaceKeywordsWithEntity(self, keywords, entity):
		keyword_copy = [entity[word] if word in entity else word for word in keywords]
		return keyword_copy

	#Replace relation synonyms with the relation name present in the database
	def replaceRelations(self):
		self.keyword_copy = self.replaceKeywordsWithEntity (self.keywords, self.relations)

	#Replace some synonyms of part of an attribute with the word present in database for eg: identities --> id 
	def replaceAttr(self):
		self.keyword_copy = self.replaceKeywordsWithEntity (self.keyword_copy, self.replace_attr)
	
	def reconstruct(self):
		self.lowercase_query = ' '.join(self.keyword_copy)

	#Method used for searching the string in reverse
	def replaceQueryTermWithEntity (self, query, entity):
		for key in entity:
			regex = '\\b' + key + '\\b'
			query = re.sub(regex, entity[key], query)
		return query

	#Replace synonyms of operators with the operator symbol
	def replaceOperators(self):
		self.lowercase_query = self.replaceQueryTermWithEntity (self.lowercase_query, self.replace_operators)

	#Replace synonyms of attributes with the actual attribute present in database employee name --> ename
	def replaceSynAttr(self):
		self.lowercase_query = self.replaceQueryTermWithEntity (self.lowercase_query, self.syn_attr)
	
	#Replace synonyms of common nouns with the actual common noun in the database
	def replaceSynCommon(self):
		self.lowercase_query = self.replaceQueryTermWithEntity (self.lowercase_query, self.syn_common)

	#search for index of operator in range start_index to end_index 
	def operatorSearch(self, start_index, end_index):
		for index in range(start_index, end_index):
			if self.isOper(self.constant_assoc[index]):
				return index
		return None

	#Return a list with the three values to append to another list
	def assignConstant (self, attribute_name, operator, constant):
		return [attribute_name, operator, constant]

	#Appending to unique or common attribute relation list
	def appendToRelationList(self, attribute_name):
		relation_list = self.attr_relations[attribute_name]
		if len(relation_list) == 1:
			if relation_list[0] not in self.unique_attribute_relation:
				self.unique_attribute_relation.append(relation_list[0])
		else:
			for relations in relation_list:						
				if relations not in self.common_attribute_relation:
					self.common_attribute_relation.append(relations)


  	#Find all constants between self.start_index and self.end_index
	def constantAssociation(self, start_index, end_index):
		self.SELECT = []

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
						if self.isAttr(self.constant_assoc[j]):
							#search for operator between the position of attribute and constant
							operator_index = self.operatorSearch(j,i)
							self.appendToRelationList(self.constant_assoc[j])

							if operator_index is None: #use default operator
								temp_list.extend(self.assignConstant(self.constant_assoc[j], self.default_operator, self.constant_assoc[i]))
								self.constant_assoc.remove(self.constant_assoc[i])
								counter += 1

							else:
								temp_list.extend(self.assignConstant(self.constant_assoc[j], self.constant_assoc[operator_index], self.constant_assoc[i]))
								self.default_operator = self.constant_assoc[operator_index] 
								self.constant_assoc.remove(self.constant_assoc[i])
								self.constant_assoc.remove(self.constant_assoc[operator_index])
								counter += 2
							break
						j = j - 1

					#if no attribute found
					if j < start_index:
						operator_index = self.operatorSearch(start_index,i)
						if operator_index is not None:
							temp_list.append(self.constant_assoc[operator_index])
							counter += 1
						temp_list.append(self.constant_assoc[i])
						self.constant_assoc.remove(self.constant_assoc[i])
						if operator_index is not None:
							self.constant_assoc.remove(self.constant_assoc[operator_index])
						counter += 1
					break

			#when no constant found break
			if match is False:
				break

			end_index = end_index - counter
			counter = 0


		#return new end_index and the list with all the elements
		return [end_index, temp_list]	

	
	def commonAssociation(self, start_index, end_index):
		self.lowercase_query = ' '.join(self.constant_assoc[start_index : end_index])
		temp_list = []
		while True:
			match = False
			for common_noun in self.common_attr:
				regex = '\\b' + common_noun + '\\b'
				found_list = re.findall(regex, self.lowercase_query)
				for found in found_list:
					match = True
					temp_list.extend(self.assignConstant(self.common_attr[found], '=', found))
					self.appendToRelationList(self.common_attr[found])
				self.lowercase_query = re.sub(regex, '', self.lowercase_query)
			if match is False:
				break
		return temp_list

	def properAssociation(self, start_index, end_index):
		self.lowercase_query = ' '.join(self.constant_assoc[start_index : end_index])
		temp_list = []
		print ('proper', self.named_entities)
		for ne in self.named_entities:
			regex = '\\b' + ne + '\\b'
			found_list = re.findall(regex, self.lowercase_query)
			flag = False
			for found in found_list:
				if found in self.proper_nouns:
					flag = True
					temp_list.extend(self.assignConstant(self.proper_nouns[found], "=", ne))
					self.appendToRelationList(self.proper_nouns[found])
			if flag:
				self.lowercase_query = re.sub(regex, '', self.lowercase_query)

		while True:
			match = False
			for name in self.proper_nouns:
				regex = '\\b' + name + '\\b'				 
				found_list = re.findall(regex, self.lowercase_query)
				for found in found_list:
					match = True
					temp_list.extend(self.assignConstant(self.proper_nouns[name], "=", found)) 
					self.appendToRelationList(self.proper_nouns[found])
				self.lowercase_query = re.sub(regex, '', self.lowercase_query)

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
	#if they are not present for a particular constant e.g eid = 25 is formed
	def assignEntity (self):
		while len(self.where_elements_list) > 0:
			if self.where_elements_index % 3 == 0:
				if not self.isAttr(self.where_elements_list[self.where_elements_index]):
					self.where_elements_list.insert(self.where_elements_index,self.default_attribute)
				self.WHERE.append(self.where_elements_list[self.where_elements_index])

			if self.where_elements_index % 3 == 1:
				if not self.isOper(self.where_elements_list[self.where_elements_index]):
					self.where_elements_list.insert(self.where_elements_index,self.default_operator)
				self.WHERE.append(self.where_elements_list[self.where_elements_index])

			if self.where_elements_index % 3 == 2:
				self.WHERE.append(self.where_elements_list[self.where_elements_index])
				if self.end_index < len(self.constant_assoc):
					self.WHERE.append(self.constant_assoc[self.end_index])
				else:
					self.WHERE.append(self.default_logical_operator)
			self.where_elements_index += 1

			if self.where_elements_index >= len(self.where_elements_list):
				break
	
	def appendCommonToWhereList(self, returned_list):
		#Traverse through the list and add default logical operator
		for index in range(len(returned_list)):
			if index % 3 == 2:
				self.WHERE.append(returned_list[index])
				self.WHERE.append(self.default_logical_operator)
			else:
				self.WHERE.append(returned_list[index])

	def andOr(self):
		self.constant_assoc = self.lowercase_query.split(' ')

		#a list with all elements of where clause along with their and/or conjunctions
		self.WHERE= []
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

				self.where_elements_list = self.returned_list[1]
				self.end_index = self.returned_list[0]
				self.where_elements_index = 0

				#traverse through the returned list and append attributes and operators in the list
				#if they are not present for a particular constant
				self.assignEntity ()

				# in case there is no constant present between self.start_index and self.end_index we won't be able to get
				# a default attribute and default operator from the self.WHERE
				if len(self.WHERE) > 0:
					self.default_attribute = self.WHERE[-4]
					self.default_operator = self.WHERE[-3]
				# We're checking for common associations and appending the returned list to self.WHERE
				#self.where_common_list = []
				self.returned_common_list = self.commonAssociation(self.start_index + 1, self.end_index)
				self.appendCommonToWhereList(self.returned_common_list)
				
				self.returned_proper_list = self.properAssociation(self.start_index + 1, self.end_index)
				self.appendCommonToWhereList(self.returned_proper_list)
				
				self.start_index = self.end_index


			self.end_index += 1
			if self.end_index >= len(self.constant_assoc):
					break

		#search again when the end of list is reached
		self.returned_list = self.constantAssociation(self.start_index + 1,self.end_index)
		self.where_elements_list = self.returned_list[1]
		self.end_index = self.returned_list[0]

		self.where_elements_index = 0
		self.assignEntity ()

		# We're checking for common associations and appending the returned list to self.WHERE
		self.where_common_list = []
		self.returned_common_list = self.commonAssociation(self.start_index + 1, self.end_index)
		self.appendCommonToWhereList(self.returned_common_list)

		self.returned_proper_list = self.properAssociation(self.start_index + 1, self.end_index)
		self.appendCommonToWhereList(self.returned_proper_list)
		self.start_index = self.end_index
		if len(self.WHERE) > 0:
			self.WHERE.pop()

	
	def backwardSearch(self, start_index, end_index):
		index = end_index - 1
		attribute_string  = self.constant_assoc[end_index]
		match = False	
		while index >= start_index:
			if self.isOper(self.constant_assoc[index]):
				i = index - 1
				while i >= start_index:
					if self.isAttr(self.constant_assoc[i]):
						#Appending to unique or common attribute relation list
						self.appendToRelationList(self.constant_assoc[i])
						#Stores index for removal of aggr attribute
						if i not in self.remove_list:
							self.remove_list.append(i)
						attribute_string = attribute_string + '(' + self.constant_assoc[i] + ')'
						match = True
						break
					i = i - 1

			if match is True:
				break
			index = index - 1
		if match is True:
			self.SELECT.append(attribute_string)
		return match

	def forwardSearch(self, start_index, end_index):
		attribute_string = self.constant_assoc[start_index]
		for index in range(start_index + 1, end_index):
			if self.isAttr(self.constant_assoc[index]):
				#Appending to unique or common attribute relation list
				self.appendToRelationList(self.constant_assoc[index])
				
				if index not in self.remove_list:
					self.remove_list.append(index)
				attribute_string = attribute_string + '(' + self.constant_assoc[index] + ')'
				break
		self.SELECT.append(attribute_string)

	def unknownAttr(self):
		#self.constant_assoc = self.lowercase_query.split(' ')
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
				if result:
					start_index = end_index + 1
					continue

				else:
					self.forwardSearch(end_index, len(self.constant_assoc)) 
					start_index = end_index + 1

			elif self.constant_assoc[index] == 'count':
				aggregate_string = 'count(*)'
				self.SELECT.append(aggregate_string)
				start_index = index + 1
		
		#Sort indices in reverse and pop from constant_assoc		
		self.remove_list.sort(reverse = True)
		for index in self.remove_list:
			self.constant_assoc.pop(index)	

		# Non aggregate attributes
		for word in self.constant_assoc:
			if self.isAttr(word):
				#Appending to unique or common attribute relation list
				self.appendToRelationList(word)
				if word not in self.SELECT:
					self.SELECT.append(word)


	#searching the remaining keywords for relations
	def relationSearch(self):
		for word in self.constant_assoc:
			if word in self.relations:
				if word not in self.unique_attribute_relation:
					self.unique_attribute_relation.append(word)
					

	def negationCheck(self):
		bool = False
		for word in self.constant_assoc:
			if word == 'not': 
				bool = True
				break
		if bool and len(self.WHERE) > 0:
			for index in range(len(self.WHERE)):
				if (index + 1) % 4 == 2:
					self.WHERE[index] = self.ant_operators[self.WHERE[index]]

	def removeDuplicates(self):
		duplicate_dict = {}
		for attr in self.SELECT:
			if attr in duplicate_dict:
				duplicate_dict[attr] += 1
			else:
				duplicate_dict[attr] = 1
		for attr in duplicate_dict:
			if duplicate_dict[attr] > 1:
				self.SELECT.remove(attr)

	def cleaningSelectList(self):
		attr_indices = []
		for index in range(len(self.SELECT)):
			if self.SELECT[index] in self.WHERE:
				attr_indices.append(index)
		if len(attr_indices) == len(self.SELECT):
			attr_indices.sort(reverse = True)
			for index in attr_indices:
				self.SELECT.pop(index)
