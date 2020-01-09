import en_core_web_sm

class ProcessedStatement():
    def __init__(self, statement):
        self.statement = statement
        self.nlp = en_core_web_sm.load()
        self.doc = self.nlp(statement)

    def location_entities(self):
        return [x for x in self.doc.ents if x.label_ in ["GPE", "LOC", "FAC"]]
    
    def climate_terms(self):
        return [x.lemma_ for x in self.doc if x.pos_ == "ADJ"]
    
    def nouns(self):
        return [x.lemma_ if x.pos_ == "NOUN" else x.norm_ for x in self.doc if x.pos_ == "NOUN" or x.suffix_ == "ing"]
    