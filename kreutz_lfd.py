import os
import sys
import nltk
from lxml import etree
from features import *
from sklearn import svm
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

def main(argv):
        trainingdir = argv[1]
        testdir = argv[2]
        languages = ['dutch', 'english', 'italian', 'spanish']
        
        for language in languages:
                # train the system
                Xtrain, Ytraingender, Ytrainage = [], [], []
                traintweets = loadData(trainingdir, language)
                traintruths = loadTruth(trainingdir, language)
                for author, tweet in traintweets.items():
                        Xtrain.extend(tweet)
                        Ytraingender.extend([traintruths[author][0]] * len(tweet))
                        Ytrainage.extend([traintruths[author][1]] * len(tweet))

                genderclf = trainGender(Xtrain, Ytraingender)
                if language == 'english' or language == 'spanish':
                        ageclf = trainAge(Xtrain, Ytrainage)


                # classify test tweets
                Xtest = []
                testtweets = loadData(testdir, language)
                outfile = open(os.path.join(testdir, language, 'truth.txt'), 'w')
                
                for author, tweet in testtweets.items():
                        Ygenderpred = genderclf.predict(tweet)
                        genderlabel = getMajority(Ygenderpred, )
                        if language == 'english' or language == 'spanish':
                                Yagepred = ageclf.predict(tweet)
                                agelabel = getMajority(Yagepred)
                        else:
                                agelabel = 'XX-XX'
                        outfile.write(':::'.join([author, genderlabel, agelabel, '\n']))

def trainGender(X, Y):
        # train the gender classifier and returns it
        features = FeatureUnion([('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(3,4))),
                                 ('malewords', SigWords('M', 1000)),
                                 ('femalewords', SigWords('F', 1000)),
                                 ('patterns', Patterns(['.','!','?','rt','#','@', 'http'])),
                                 ('capitals', Capitals()),])

        clf = svm.LinearSVC()                              
        pipeline = Pipeline([('features', features), ('classifier', clf)])
        pipeline.fit(X, Y)
        return pipeline

def trainAge(X, Y):
        # train the age classifier and returns it
        features = FeatureUnion([('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(3,4))),
                                 ('agewords1', SigWords('18-24', 1000)),
                                 ('agewords2', SigWords('25-34', 1000)),
                                 ('agewords3', SigWords('35-49', 1000)),
                                 ('agewords4', SigWords('50-XX', 1000)),
                                 ('patterns', Patterns(['.','!','?','rt','#','@', 'http'])),
                                 ('capitals', Capitals())],
                                transformer_weights={'tfidf': 3})
        clf = svm.LinearSVC()
        pipeline = Pipeline([('features', features), ('classifier', clf)])
        pipeline.fit(X, Y)
        return pipeline
        
def getMajority(Y):
        # returns the majority label in an array-like
        Y = [y for y in Y]
        majority = max(set(Y), key=Y.count)
        return majority
           
def loadData(directory, language):
        # returns a dictionary of tweets per author
        tweets = {}
        languagedir = os.path.join(directory, language)
        for filename in os.listdir(languagedir):
                if filename.endswith('xml'):
                        handle = open(os.path.join(languagedir, filename), 'rb')
                        tree = etree.fromstring(handle.read())
                        documents = tree.xpath('//document')
                        tweets[filename[:-4]] = [doc.text.rstrip() for doc in documents]
        return tweets

def loadTruth(directory, language):
        # returns a dictionary of truth values per author
        truths = {}
        filepath = os.path.join(directory, language, 'truth.txt')
        handle = open(filepath, 'r')
        for line in handle:
                split = line.split(':::')
                truths[split[0]]=(split[1],split[2])
        return truths
        

if __name__ == '__main__':
        main(sys.argv)
