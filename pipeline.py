import spacy
import en_core_web_sm
import nltk
from nltk.corpus import wordnet as wn
from travelrec.similarity import (
    ClimateSimilarity,
    GeoFeaturesSimilarity,
    ActvitySimilarity,
)
from travelrec.sparql import (
    get_location,
    get_cities_with_temperature,
    get_geofeatures,
    get_activities,
)


nltk.download("wordnet", quiet=True)
nlp = en_core_web_sm.load()

examples = [
    "mild places near Paris with mountains for swimming",
]

climateSim = ClimateSimilarity()
geoSim = GeoFeaturesSimilarity()
activitySim = ActvitySimilarity()

for example in examples:
    print(f"Query: {example}")
    doc = nlp(example)
    # location specification
    location_entities = [x for x in doc.ents if x.label_ in ["GPE", "LOC"]]
    print(f"Locations: {location_entities}")

    loc = location_entities[0].text
    latitude, longitude = get_location(loc)
    print(f"Coordinates: {loc} - ({latitude}, {longitude})")

    # climate filters
    climate_predicates = climateSim.construct_filters(
        [x.lemma_ for x in doc if x.pos_ == "ADJ"]
    )
    climate_predicate = climate_predicates[0]
    print(f"Climate: {climate_predicate}")
    nearby_cities = get_cities_with_temperature(
        latitude, longitude, 150, climate_predicate
    )
    print(
        f"Found {len(nearby_cities)} cities nearby: {[x for _, _, x in nearby_cities]}"
    )

    # geofeatures ranking
    nouns = [x.lemma_ for x in doc if x.pos_ == "NOUN"]
    geofeatures_codes = geoSim.construct_filters(nouns)
    print(f"Looking for geofeatures: {geofeatures_codes}")

    # activities ranking
    activities_codes = activitySim.construct_filters(nouns)
    print(f"Looking for activities: {activities_codes}")

    results = []
    print("Calculating scores...")
    for city_latitude, city_longitude, city_name in nearby_cities:
        geo_results = get_geofeatures(
            city_latitude, city_longitude, 350, geofeatures_codes
        )
        geofeatures_count = len(geo_results["results"]["bindings"])

        activity_results = get_activities(
            city_latitude, city_longitude, 4300, activities_codes
        )
        activities_count = len(activity_results["results"]["bindings"])

        ranking_points = 2 * geofeatures_count + activities_count
        print(f"\t{city_name} with {ranking_points} points")
        results.append((city_name, ranking_points))

    print(f"Final ranking: {[x for x, _ in sorted(results, key=lambda x: -x[1])]}")

