from travelrec.similarity import ClimateSimilarity

import unittest

class TestSimilarity(unittest.TestCase):

    def test_climate_similarity(self):
        climateSim = ClimateSimilarity()
        words = ['mild', 'medium', 'warm', 'hot']
        correct_synonym = ['mild', 'mild', 'warm', 'warm']

        filters = climateSim.construct_filters(words)

        self.assertEqual(len(words), len(filters), 'number of filters is wrong')

        for i in range(0, len(words)):
            self.assertEqual(climateSim._mapping[correct_synonym[i]], filters[i], f'wrong synonym for {words[i]}')

