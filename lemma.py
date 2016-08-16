from nltk.stem import WordNetLemmatizer

class Lemma:
    def __init__(self):
        self.wordnet_lemmatizer = WordNetLemmatizer()

    def queryLemmatize(self, query):    
        sent_tok = query.split(" ")
        final = []
        for words in sent_tok:
            if words != 'less':
                final.append(self.wordnet_lemmatizer.lemmatize(words))
            else: 
                final.append(words)
        final_str = " ".join(final)
        return final_str
        
        #return self.wordnet_lemmatizer.lemmatize(query)

