from travelrec.similarity import ActvitySimilarity, ClimateSimilarity, GeoFeaturesSimilarity

import unittest
from travelrec.processed_statement import ProcessedStatement

class TestSimilarity(unittest.TestCase):

    def test_climate_similarity(self):
        climateSim = ClimateSimilarity()
        words = ['mild', 'warm']#, 'medium', 'hot']
        correct_synonym = ['mild', 'warm']#, 'mild', 'warm']

        filters = climateSim.construct_filters(words)

        self.assertEqual(len(words), len(filters), 'number of filters is wrong')

        for synonym, filter, word in zip(correct_synonym, filters, words):
            self.assertEqual(climateSim._mapping[synonym], filter, f'wrong synonym for {word}')

    def test_geo_features_similarity(self):
        geoFeaturesSim = GeoFeaturesSimilarity()
        examples = ["swimming in Cracow", "mountains near Statue of Liberty", "lakes in Mazury", "mountains and lakes in Poland"]
        results = [[], ["T.MT", "T.MTS"], ["H.LK", "H.LKS"], ["T.MT", "T.MTS", "H.LK", "H.LKS"]]

        for example, result in zip(examples, results):
            processed_statement = ProcessedStatement(example)
            nouns = processed_statement.nouns()

            similarities = geoFeaturesSim.construct_filters(nouns)

            self.assertListEqual(sorted(similarities), sorted(result))

    def test_actvity_similarity(self):
        activitySim = ActvitySimilarity()
        examples = ["mountains near Statue of Liberty", "basketball in Cracow", "a ZOO and gym near Statue of Liberty", "cinemas in Mazury", "swimming in Poland"]
        results = [[], ["BASKETBALL"], ["ZOO", "GYM"], ["CINEMA"], ["SWIMMING"]]

        for i in range(0, len(examples)):
            example = examples[i]
            processed_statement = ProcessedStatement(example)
            nouns = processed_statement.nouns()

            similarities = activitySim.construct_filters(nouns)

            self.assertEqual(len(similarities), len(results[i]))
            for res in results[i]:
                self.assertTrue(res in similarities, f"{res} is not in activity filters for '{example}'")
