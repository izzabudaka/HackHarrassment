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
    def get_smt(self, tokens, labels):
        stmt = topbox.STMT('harrass_lda', epochs=10, mem=15000)

        stmt.train(tokens, labels)
        return stmt

    def get_model(self):
        reader.read_labels()
        reader.read_data_files()
        convo_ids = reader.get_all_convos()

        words = reader.read_bad_words()
        labels, tokens, true_class = text_mining.tokenize_words(convo_ids, reader.conversation_text,
                                                                reader.conversation_labels, set(words))
        smt = get_smt(tokens, labels)
        return smt
