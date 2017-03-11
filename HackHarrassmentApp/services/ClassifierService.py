class ClassifierService:
    def classify(self, distributions):
        result = []
        for dist in distributions:
            current = sum(list(dist))
            if current >= 1.0:
                result.append(1)
            else:
                result.append(0)
        return result


