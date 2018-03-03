import pickle


class Model:

    def __init__(self, estimator):
        self._estimator = estimator

    @classmethod
    def from_pickle(cls, pickle_object_path):
        estimator = pickle.load(open(pickle_object_path, 'rb'))
        return cls(estimator)

    def _fit(self, data):
        self._estimator.fit(data)

    def predict(self, data):
        prediction = self._estimator.predict(data)
        return prediction
