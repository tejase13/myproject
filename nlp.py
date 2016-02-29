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
	
		#Original Query	
		self.original_query = query

		#Stop words list
		self.stop_words= list(stopwords.words("english"))
		self.stop_words.remove('of')
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

	def tokenize(self):
		self.lowercase_query = self.original_query.lower()
		self.words = WordPunctTokenizer().tokenize(self.lowercase_query)
		self.punct_list = list(string.punctuation)
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
				self.keyword_copy[index] = self.relations[self.keywords[index]]	def replaceAttr(self):
		length = len(self.keywords)
		for index in range(length):
			if self.keywords[index] in self.replace_attr:
				self.keyword_copy[index] = self.replace_attr[self.keywords[index]]

	def reconstruct(self):
		self.lowercase_query = ' '.join(self.keyword_copy)

	def replaceSynAttr(self):
		for key in self.syn_attr:
			if self.lowercase_query.find(key) != -1:
				self.lowercase_query = self.lowercase_query.replace(key, self.syn_attr[key])

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
					while j > 0:
						if self.constant_assoc[j] in self.attr_relations:
							self.WHERE[self.constant_assoc[j]] = self.constant_assoc[i]
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

	def unknownAttr(self):
		for index in self.constant_assoc:
			if index in self.attr_relations:
				rel = self.attr_relations[index]
				for value in rel:
					if value in self.FROM:
						self.FROM[value] += 1
					else:
						self.FROM[value] = 1
				self.SELECT.append(index)



						
