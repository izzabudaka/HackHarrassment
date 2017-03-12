from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from HackHarrassmentApp.services.ClassifierService import ClassifierService
from HackHarrassmentApp.services.NLPService import NLPService
from HackHarrassmentApp.services.ReaderService import ReaderService

reader = ReaderService()
text_mining = NLPService()
classifer = ClassifierService()
stop = set(stopwords.words('english'))


class DetectionService:
    def __init__(self, model, svm, tfidf_vect):
        self.model = model
        self.svm = svm
        self.tfidf_vect = tfidf_vect
        self.labels = reader.read_bad_words()
        self.labels_str = " ".join(self.labels)
        self.toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)

    def is_harrassment(self, text):
        text = text.lower()
        tokens = self.toker.tokenize(text)
        tokens = [i for i in tokens if i not in stop]
        labels = text_mining.get_label(tokens, self.labels)
        self.model.test([" ".join(tokens).strip()], [" ".join(labels).strip()])
        _, topic_dist = self.model.results([self.labels_str])
        if len(labels) > 0:
            return 1
        result = classifer.classify(topic_dist)
        return result[0] if len(result) > 0 else 0

    def is_harrassment_svm(self, text):
        text = text.lower()
        tokens = self.toker.tokenize(text)
        tokens = [i for i in tokens if i not in stop]
        post = " ".join(tokens).strip()
        tfidf_test = self.tfidf_vect.transform([post])
        predicted = self.svm.predict(tfidf_test)
        return predicted[0]
