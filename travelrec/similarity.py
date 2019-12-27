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
    """Based on GeoNames codes: https://www.geonames.org/export/codes.html
    """

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


class ActvitySimilarity(BaseSimiliarity):
    """Based on SLIPO codes: 
    https://github.com/SLIPO-EU/TripleGeo/blob/master/test/classification/OSM_POI_sample_classification.csv
    """

    def __init__(self):
        super().__init__()

    def construct_filters(self, words):
        top_words = []
        features = [x.lower() for x in ["ARCHERY", "BASEBALL"]]
        for word in words:
            for feature in features:
                a = wn.synsets(word)[0]
                b = wn.synsets(feature)[0]

                similarity = a.path_similarity(b)
                if similarity is not None and similarity > 0.8:
                    top_words.append(feature)

        return top_words
