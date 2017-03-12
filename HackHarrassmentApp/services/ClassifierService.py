class ClassifierService:
    def classify(self, distributions):
        result = []
        for dist in distributions:
            current = 0
            for val in dist:
                if val > 0.95:
                    current = 1
            result.append(current)
        return result


