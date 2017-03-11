from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


class EvaluatorService:
    def __init__(self):
        self.scores = []

    def average(self):
        total_f = 0.0
        total_acc = 0.0
        total_p = 0.0
        total_r = 0.0
        for val in self.scores:
            total_acc += val["accuracy"]
            total_f += val["f_score"]
            total_p += val["precision"]
            total_r += val["recall"]

        print()
        print("AVERAGES")
        print("F1 Score: " + str(total_f/float(len(self.scores))))
        print("Accuracy: " + str(total_acc/float(len(self.scores))))
        print("Precision: " + str(total_p/float(len(self.scores))))
        print("Recall: " + str(total_r/float(len(self.scores))))

    def evalute(self, classification, predictions):
        if len(predictions) > len(classification):
            predictions = predictions[:len(classification)]
        elif len(classification) > len(predictions):
            classification = classification[:len(predictions)]
        print("F1 Score: " + str(f1_score(classification, predictions, average="macro")))
        print("Accuracy: " + str(accuracy_score(classification, predictions)))
        print("Precision: " + str(precision_score(classification, predictions, average="macro")))
        print("Recall: " + str(recall_score(classification, predictions, average="macro")))
        res = {"f_score": f1_score(classification, predictions, average="macro"),
                "accuracy": accuracy_score(classification, predictions),
                "precision": precision_score(classification, predictions, average="macro"),
                "recall": recall_score(classification, predictions, average="macro")}
        self.scores.append(res)
        return res
