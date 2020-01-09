import unittest
import en_core_web_sm
from travelrec.processed_statement import ProcessedStatement

class TestProcessedStatement(unittest.TestCase):

    def test_location_entities(self):
        examples = ["hot place in Paris", "sightseeing in Cracow", "swimming near Eiffel Tower", "swimming near Statue of Liberty", "warm place in the Tatra Mountains"]
        results = ["Paris", "Cracow", "Eiffel Tower", "Statue of Liberty", "the Tatra Mountains"]
        for i in range(0, len(examples)):
            example = examples[i]
            processed_statement = ProcessedStatement(example)
            location_entities = processed_statement.location_entities()

            self.assertEqual(len(location_entities), 1)
            self.assertEqual(location_entities[0].text, results[i])
    
    def test_nouns(self):
        examples = ["sightseeing in Cracow", "mountains near Statue of Liberty", "lakes in Mazury", "swimming in Poland"]
        results = ["sightseeing", "mountain", "lake", "swimming"]
        for i in range(0, len(examples)):
            example = examples[i]
            processed_statement = ProcessedStatement(example)
            nouns = processed_statement.nouns()

            self.assertTrue(results[i] in nouns, f"noun in '{example}': found {nouns}, expected: {results[i]}")

    def test_climate_terms(self):
        examples = ["warm places", "snowy resort in Alps", "city in Poland with mild temperature"]
        results = ["warm", "snowy", "mild"]
        for i in range(0, len(examples)):
            example = examples[i]
            processed_statement = ProcessedStatement(example)
            climate_terms = processed_statement.climate_terms()

            self.assertEqual(len(climate_terms), 1)
            self.assertEqual(climate_terms[0], results[i])
