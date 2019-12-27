import spacy
import en_core_web_sm
import nltk
from nltk.corpus import wordnet as wn
from travelrec.similarity import TemperatureSimilarity, GeoFeaturesSimilarity

nltk.download("wordnet", quiet=True)
nlp = en_core_web_sm.load()

examples = [
    "warm places in Poland",
    "cold places near Cracov",
    "places with beaches",
    "lakes in Italy",
    "warm places with desert",
    "mild temperatures near rivers in Poland",
    "skiing in France and sunny",
    "swimming beaches in Italy",
    "sailing warm Poland",
    "cities worth sightseeing near Berlin",
]

tempSim = TemperatureSimilarity()
geoSim = GeoFeaturesSimilarity()

for example in examples:
    print(f"------------------------\n{example}")
    doc = nlp(example)

    # temperature words
    print(tempSim.construct_filters([x.lemma_ for x in doc if x.pos_ == "ADJ"]))

    # area words
    print(geoSim.construct_filters([x.lemma_ for x in doc if x.pos_ == "NOUN"]))

    # location specification
    for ent in [x for x in doc.ents if x.label_ in ["GPE", "LOC"]]:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
