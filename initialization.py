#! /usr/bin/python3

import string
import shelve,time
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordPunctTokenizer

class Initialization:
	
	def initializeStopWords(self):
		#initialize stopwords 
		#remove some of them
		self.stop_words = list(stopwords.words("english"))
		self.stop_words.remove('of')
		self.stop_words.remove('not')
		self.stop_words.remove('is')
		self.stop_words.remove('nor')
		self.stop_words.remove('and')
		self.stop_words.remove('or')
		self.stop_words.remove('but')
		self.stop_words.remove('did')
		self.stop_words.remove('more')
		self.stop_words.remove('most')
		self.stop_words.remove('where')
		self.stop_words.remove('who')
		self.stop_words.remove('what')
		self.stop_words.remove('which')
		self.stop_words.remove('how')
		self.stop_words.remove('when')
		self.stop_words.remove('above')
		self.stop_words.remove('below')
		self.stop_words.remove('before')
		self.stop_words.remove('after')
		self.stop_words.remove('me')

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

		return self.stop_words

	def initializePunctList(self):
		self.punct_list = list(string.punctuation)
		self.punct_list.remove('<')
		self.punct_list.remove('>')
		self.punct_list.remove('!')
		self.punct_list.remove('=')
		self.punct_list.remove('*')
		self.punct_list.remove('/')

		return self.punct_list
