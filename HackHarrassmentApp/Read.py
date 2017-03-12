import os
import re
import shutil
import sys

from sklearn.model_selection import KFold

import topbox
from HackHarrassmentApp.services.ClassifierService import ClassifierService
from HackHarrassmentApp.services.NLPService import NLPService
from HackHarrassmentApp.services.ReaderService import ReaderService
from HackHarrassmentApp.services.EvalutatorService import EvaluatorService

reader = ReaderService()
text_mining = NLPService()
classifer = ClassifierService()
evaluator = EvaluatorService()


def get_smt(tokens, labels):
    stmt = topbox.STMT('harrass_lda', epochs=10, mem=15000)

    stmt.train(tokens, labels)
    return stmt


def get_splits(all_convos, harrassment_convos, labels, tokens, true_class):
    skf = KFold(n_splits=10)
    classifications = [[1] if convo in harrassment_convos else [0] for convo in all_convos]
    idxs = skf.split(classifications, all_convos)

    test_folds = []
    test_folds_labels = []
    train_folds = []
    train_folds_labels = []
    test_true_labels = []

    for fold in idxs:
        test_current = []
        test_current_labels = []
        train_current = []
        train_current_labels = []
        test_true_labels_current = []
        for idx in fold[0]:
            train_current.append(" ".join(tokens[idx]))
            train_current_labels.append(" ".join(labels[idx]))
        for idx in fold[1]:
            if len(labels[idx]) > 0:
                test_current.append(" ".join(tokens[idx]))
                test_current_labels.append(" ".join(labels[idx]))
                test_true_labels_current.append(true_class[idx])
        test_folds.append(test_current)
        test_folds_labels.append(test_current_labels)
        train_folds.append(train_current)
        train_folds_labels.append(train_current_labels)
        test_true_labels.append(test_true_labels_current)

    return train_folds_labels, train_folds, test_folds_labels, test_folds, test_true_labels


def main(argv):
    reader.read_labels()
    reader.read_data_files()
    reader.read_other_data_file()

    convo_ids = reader.get_all_convos()
    harrass_convos = reader.get_harrassment_convos()

    words = reader.read_bad_words()
    labels, tokens, true_class = text_mining.tokenize_words(convo_ids, reader.conversation_text,
                                                            reader.conversation_labels, set(words))
    train_labels, train_tokens, test_labels, test_tokens, test_true_class = get_splits(convo_ids, harrass_convos,
                                                                                       labels, tokens, true_class)
    for idx in range(10):
        for f in os.listdir('../topbox/box/'):
            if re.search(".*.gz", f):
                os.remove(os.path.join('../topbox/box/', f))
        try:
            shutil.rmtree('../topbox/box/harrass_lda_train')
        except:
            pass
        smt = get_smt(train_tokens[idx], train_labels[idx])
        c_tokens = test_tokens[idx]
        l_tokens = test_labels[idx]
        smt.test(c_tokens, l_tokens)
        _, topic_dist = smt.results(test_labels[idx])
        predictions = classifer.classify(topic_dist)
        true_classes = test_true_class[idx]
        evaluator.evalute(true_classes, predictions)
    evaluator.average()


if __name__ == "__main__":
    main(sys.argv)
