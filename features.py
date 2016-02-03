from collections import defaultdict
from sklearn.base import BaseEstimator, TransformerMixin

def tokenize(text):
        # returns only lowered characters and spaces for a string
        text = text.lower()
        newtext = ''
        for ch in text:
                if ch in 'abcdefghijklmnopqrstuvwxyz ':
                        newtext += ch
        return newtext

class Capitals(BaseEstimator, TransformerMixin):
        # feature that counts capitalized characters in a tweet
        def fit(self, X, Y=None):
                return self
        def transform(self, X):
                return [[sum(1 for ch in doc if ch.isupper())] for doc in X]

class Patterns(BaseEstimator, TransformerMixin):
        # feature that counts occurences for a range of patterns
        def __init__(self, patterns):
                self.patterns = patterns
        def fit(self, X, Y=None):
                return self
        def transform(self, X):
                return [[doc.lower().count(pattern)/len(doc) for pattern in self.patterns] for doc in X]

class SigWords(BaseEstimator, TransformerMixin):
        # feature that calculates the ratio between word occurrence in male and female tweets
        def __init__(self, sig, number):
                self.sig = sig
                self.number = number
                self.sigwords = []
                self.dict1, self.dict2 = defaultdict(int), defaultdict(int)
                
        def fit(self, X, Y=None):
                for i in range(len(X)):
                        tokens = self.process(X[i])
                        if Y[i] == self.sig:
                                for token in tokens:
                                        self.dict1[token]+=1
                        else:
                                for token in tokens:
                                        self.dict2[token]+=1
                for token in self.dict1:
                        self.sigwords.append(((self.dict2[token]+1)/(self.dict1[token]+1),token))
                self.sigwords.sort()
                self.sigwords = self.sigwords[:self.number]
                return self

        def process(self, doc):
                return tokenize(doc).split()

        def transform(self, X):
                tokendocs = [tokenize(doc).split() for doc in X]
                return [[score*tokens.count(sigword) for score, sigword in self.sigwords] for tokens in tokendocs]
