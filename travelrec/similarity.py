from abc import ABC, abstractmethod
from nltk.corpus import wordnet as wn
from travelrec.constants import get_slipo_codes, get_geonames_codes


class BaseSimiliarity(ABC):
    def __init__(self):
        super().__init__()


class ClimatePredicate:
    def __init__(self, property_name, field_name, predicates):
        self.property_name = property_name
        self.field_name = field_name
        self.predicate = " && ".join(
            [f"{field_name} {predicate}" for predicate in predicates]
        )

    def __repr__(self):
        return self.predicate


class ClimateSimilarity(BaseSimiliarity):
    def __init__(self):
        super().__init__()
        self._mapping = {
            "cold": ClimatePredicate("yearMeanC", "?yearMeanC", ["<5"]),
            "mild": ClimatePredicate("yearMeanC", "?yearMeanC", [">5", "<15"]),
            "warm": ClimatePredicate("yearMeanC", "?yearMeanC", [">15"]),
        }

    def construct_filters(self, words):
        top_words = []

        for word in words:
            best_synonym = ''
            best_similarity = 0
            for feature in self._mapping.keys():
                for a in wn.synsets(word):
                    for b in wn.synsets(feature):
                        similarity = a.path_similarity(b)
                        if similarity is not None and similarity > best_similarity:
                            best_synonym = feature
                            best_similarity = similarity

            if best_similarity > 0.8:
                top_words.append(best_synonym)
            else:
                top_words.append(None)

        all_predicates = []
        for feature in top_words:
            if feature is not None:
                all_predicates.append(self._mapping[feature])
            else:
                all_predicates.append(None)

        return all_predicates


class GeoFeaturesSimilarity(BaseSimiliarity):
    """Based on GeoNames codes: https://www.geonames.org/export/codes.html
    """

    def __init__(self):
        super().__init__()
        self._mapping = get_geonames_codes()

    def construct_filters(self, words):
        top_words = []

        for word in words:
            for feature in self._mapping.keys():
                a = wn.synsets(word)[0]
                b = wn.synsets(feature)[0]

                similarity = a.path_similarity(b)
                if similarity is not None and similarity > 0.8:
                    top_words.append(feature)

        all_codes = []
        for feature in top_words:
            all_codes.extend(self._mapping[feature])

        return all_codes


class ActvitySimilarity(BaseSimiliarity):
    """Based on SLIPO codes: 
    https://github.com/SLIPO-EU/TripleGeo/blob/master/test/classification/OSM_POI_sample_classification.csv
    """

    def __init__(self):
        super().__init__()
        self._mapping = get_slipo_codes()

    def construct_filters(self, words):
        top_words = []
        for word in words:
            for feature in self._mapping.keys():
                a = wn.synsets(word)[0]
                b = wn.synsets(feature)[0]

                similarity = a.path_similarity(b)
                if similarity is not None and similarity > 0.8:
                    top_words.append(feature)

        all_codes = []
        for feature in top_words:
            all_codes.append(self._mapping[feature])

        return all_codes
