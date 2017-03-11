from HackHarrassmentApp.services.ClassifierService import ClassifierService
from HackHarrassmentApp.services.NLPService import NLPService
from HackHarrassmentApp.services.ReaderService import ReaderService
from nltk import word_tokenize

reader = ReaderService()
text_mining = NLPService()
classifer = ClassifierService()

class DetectionService:
    def __init__(self, model):
        self.model = model
        self.labels = reader.read_bad_words()

    def is_harrassment(self, text):
        tokens = word_tokenize(text)
        labels = text_mining.get_label(tokens, self.labels)
        self.model.test(" ".join(tokens), " ".join(labels))
        topic_dist = self.model.results(" ".join(labels))
        return classifer.classify(topic_dist)
