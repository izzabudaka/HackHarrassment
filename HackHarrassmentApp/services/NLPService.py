from nltk import word_tokenize
from fuzzywuzzy import fuzz


class NLPService:
    def __init__(self):
        pass

    def get_sentiment(self, text):
        pass

    def fuzzy_match(self, w1, w2):
        return fuzz.ratio(w1, w2)

    def get_labels(self, docs, labels):
        all_labels = []
        for tokens in docs:
            all_labels.append(self.get_label(tokens, labels))
        return all_labels

    def get_label(self, tokens, labels):
        current_labels = []
        for token in tokens:
            if token in labels:
                current_labels.append(token)
        return current_labels

    def tokenize_words(self, convo_ids, convo_texts, convo_labels, all_labels):
        tokens = []
        true_class = []
        for c_id in convo_ids:
            tokens.append(word_tokenize(convo_texts[c_id]))
            true_class.append(1 if convo_labels[c_id] == 'Y' else 0)
        labels = self.get_labels(tokens, all_labels)
        return labels, tokens, true_class

    def get_entities(self, text):
        pass
