import unittest
import en_core_web_sm

class TestNlp(unittest.TestCase):

    def test_location_entities(self):
        example = "hot place in Paris"
        nlp = en_core_web_sm.load()
        doc = nlp(example)
        # location specification
        location_entities = [x for x in doc.ents if x.label_ in ["GPE", "LOC"]]

        self.assertEqual(len(location_entities), 1)
        self.assertEqual(location_entities[0].text, "Paris")
