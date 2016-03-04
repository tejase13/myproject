#! /usr/bin/python3

import string
import shelve
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

	def replaceRelations(self):
		self.keyword_copy = list(self.keywords)
		length = len(self.keywords)
		for index in range(length):
			if self.keywords[index] in self.relations:
				self.keyword_copy[index] = self.relations[self.keywords[index]]	
	
	def replaceAttr(self):
		length = len(self.keywords)
		for index in range(length):
			if self.keywords[index] in self.replace_attr:
				self.keyword_copy[index] = self.replace_attr[self.keywords[index]]

	def reconstruct(self):
		self.lowercase_query = ' '.join(self.keyword_copy)

	def replaceOperators(self):
		for key in self.replace_operators:
			if self.lowercase_query.find(key) != -1:
				self.lowercase_query = self.lowercase_query.replace(key, self.replace_operators[key])

	def replaceSynAttr(self):
		for key in self.syn_attr:
			if self.lowercase_query.find(key) != -1:
				self.lowercase_query = self.lowercase_query.replace(key, self.syn_attr[key])
	
	def replaceSynCommon(self):
		for key in self.syn_common:
			if self.lowercase_query.find(key) != -1:
				self.lowercase_query = self.lowercase_query.replace(key, self.syn_common[key])
	
	def operatorSearch(self, j, i):
		for index in range(j,i):
			if self.constant_assoc[index] in self.operator_list:
				return self.constant_assoc[index]

	def constantAssociation(self):
		self.SELECT = []
		self.WHERE= {}
		self.FROM = {}
		self.constant_assoc = self.lowercase_query.split(' ')
		while True:
			match = False
			for i in range(len(self.constant_assoc)):
				if self.constant_assoc[i].isdigit():
					j = i - 1
					match = True
					while j >= 0:
						if self.constant_assoc[j] in self.attr_relations:
							operator = self.operatorSearch(j,i)
							if self.constant_assoc[j] in self.WHERE:  # if attribute already exists in WHERE dictionary append to the list of values associated with that attributed
								val_list = self.WHERE[self.constant_assoc[j]]
								val_list.append(operator)
								val_list.append(self.constant_assoc[i])
								self.WHERE[self.constant_assoc[j]] = val_list
							else:  # if attribute does not exist in dictionary then make new list and add
								val_list = [operator,self.constant_assoc[i]]
								self.WHERE[self.constant_assoc[j]] = val_list

							# increasing count in FROM dictionary
							rel = self.attr_relations[self.constant_assoc[j]]
							for value in rel:
								if value in self.FROM:
									self.FROM[value] += 1
								else:
									self.FROM[value] = 1
							self.constant_assoc.remove(self.constant_assoc[i])
							self.constant_assoc.remove(self.constant_assoc[j])
							break
						j = j - 1
					break
			
			if match is False:
				break

	
	def commonAssociation(self):
		self.lowercase_query = ' '.join(self.constant_assoc)
		while True:
			match = False
			for key in self.common_attr:
				if self.lowercase_query.find(key) != -1:
					match = True
					# similar implementation to the above method dealing with duplicates in FROM dictionary
					if self.common_attr[key] in self.WHERE:
						val_list = self.WHERE[self.common_attr[key]]
						val_list.append(key)
						self.WHERE[self.common_attr[key]] = val_list
					else:
						val_list = [key]
						self.WHERE[self.common_attr[key]] = val_list 

					rel = self.attr_relations[self.common_attr[key]]
					for value in rel:
						if value in self.FROM:
							self.FROM[value] += 1
						else:
							self.FROM[value] = 1
					self.lowercase_query = self.lowercase_query.replace(key,'')

			if match is False:
				break


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
