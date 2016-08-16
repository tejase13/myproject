import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tree import Tree
import shelve
class NER:
    """docstring for ClassName"""
    def __init__(self, query):
        self.original_query = query
       	conf = shelve.open('conf') 
        self.train_text = conf['train_text']
        self.custom_sent_tokenizer = PunktSentenceTokenizer(self.train_text)
        self.tokenized = self.custom_sent_tokenizer.tokenize(self.original_query)

    def processContent(self):
        try:
            for i in self.tokenized:
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(words)
                namedEnt = nltk.ne_chunk(tagged, binary=True)
                #print(namedEnt)
                #namedEnt.draw()
            return namedEnt
        except Exception as e:
            print(str(e))
        

    # Parse named entities from tree
    def structureNamedEntities(self):
    	ne = []
    	for subtree in self.named_entity_tree:
    		if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
    			ne_label = subtree.label()
    			ne_string = " ".join([token for token, pos in subtree.leaves()])
    			ne.append((ne_string, ne_label))
    	return ne

    def performNER(self):
        self.named_entity_tree = self.processContent()
        #print(type(self.named_entity_tree))
        self.named_entity_tuple = self.structureNamedEntities()
        #print(ne)
        names = [element[0] for element in self.named_entity_tuple]
        return names
