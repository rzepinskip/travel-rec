import en_core_web_sm
from travelrec.recommendations_pipeline import recommendations_pipeline

nlp = en_core_web_sm.load()

examples = [
    # "places for swimming near Paris",
    # "places near Paris with mountains for swimming",
    # "mild places near Paris with mountains for swimming",
    "cold or mild places near Viena",
]

for example in examples:
    recommendations_pipeline(example, nlp, True)
