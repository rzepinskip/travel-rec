from abc import ABC, abstractmethod
from nltk.corpus import wordnet as wn


class BaseSimiliarity(ABC):
    def __init__(self):
        super().__init__()


class TemperatureSimilarity(BaseSimiliarity):
    def __init__(self):
        super().__init__()

    def construct_filters(self, words):
        top_words = []

        for word in words:
            for feature in ["warm", "cold"]:
                a = wn.synsets(word)[0]
                b = wn.synsets(feature)[0]

                similarity = a.path_similarity(b)
                if similarity is not None and similarity > 0.8:
                    top_words.append(feature)

        return top_words


class GeoFeaturesSimilarity(BaseSimiliarity):
    def __init__(self):
        super().__init__()

    def construct_filters(self, words):
        top_words = []

        for word in words:
            for feature in ["beach", "desert"]:
                a = wn.synsets(word)[0]
                b = wn.synsets(feature)[0]

                similarity = a.path_similarity(b)
                if similarity is not None and similarity > 0.8:
                    top_words.append(feature)

        return top_words
