import os
import re
import shutil

from sklearn import svm

import topbox
from HackHarrassmentApp.services.ClassifierService import ClassifierService
from HackHarrassmentApp.services.EvalutatorService import EvaluatorService
from HackHarrassmentApp.services.NLPService import NLPService
from HackHarrassmentApp.services.ReaderService import ReaderService

reader = ReaderService()
text_mining = NLPService()
classifer = ClassifierService()
evaluator = EvaluatorService()


class Model:
    def __init__(self, tfidf_vect):
        self.BOX_DIR = self.RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../../topbox/box/"
        self.tfidf_vect = tfidf_vect
        reader.read_labels()
        reader.read_data_files()
        reader.read_other_data_file()

    def get_svm_l(self, posts, labels):
        tfidf_trans = self.tfidf_vect.fit_transform(posts)
        tfidf_classifier = svm.SVC()
        tfidf_classifier.fit(tfidf_trans, labels)
        return tfidf_classifier

    def clean(self):
        for f in os.listdir(self.BOX_DIR):
            if re.search(".*.gz", f):
                os.remove(os.path.join(self.BOX_DIR, f))
        try:
            shutil.rmtree(self.BOX_DIR + 'harrass_lda_train')
        except:
            pass

    def get_smt(self, tokens, labels):
        stmt = topbox.STMT('harrass_lda', epochs=10, mem=15000)
        str_tokens = []
        str_labels = []
        for i in range(len(tokens)):
            str_tokens.append(" ".join(tokens[i]))
            str_labels.append(" ".join(labels[i]))
        stmt.train(str_tokens, str_labels)
        return stmt

    def get_svm(self):
        convo_ids = reader.get_all_convos()
        words = reader.read_bad_words()
        labels, tokens, true_class = text_mining.tokenize_words(convo_ids, reader.conversation_text,
                                                                reader.conversation_labels, set(words))
        for i in range(len(tokens)):
            tokens[i] = " ".join(tokens[i])
        svm = self.get_svm_l(tokens, true_class)
        return svm

    def get_model(self):
        convo_ids = reader.get_all_convos()
        words = reader.read_bad_words()
        labels, tokens, true_class = text_mining.tokenize_words(convo_ids, reader.conversation_text,
                                                                reader.conversation_labels, set(words))
        smt = self.get_smt(tokens, labels)
        return smt
