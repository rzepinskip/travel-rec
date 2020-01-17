import logging
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
from travelrec.processed_statement import ProcessedStatement
from travelrec.scoring import score_cities_parallelly

search_distances = {
    'climate': 300,
    'geofeatures': 150,
    'activities': 75
}

class NoLocationsFoundError(Exception):
    """Raised when no locations were found based on provided query"""
    pass

def recommendations_pipeline(query, nlp, verbose=False):
    if verbose:
        logging.basicConfig(level=logging.INFO)
    climateSim = ClimateSimilarity()
    geoSim = GeoFeaturesSimilarity()
    activitySim = ActvitySimilarity()

    logging.info(f"Query: {query}")
    processed_statement = ProcessedStatement(query)
    # location specification
    location_entities = processed_statement.location_entities()
    logging.info(f"Locations: {location_entities}")

    if len(location_entities) == 0:
        raise NoLocationsFoundError

    location_coordinates = [get_location(loc.text) for loc in location_entities]
    logging.info("Coordinates:")
    for loc, coord in zip(location_entities, location_coordinates):
        logging.info(f"\t{loc} - ({coord[0]}, {coord[1]})")

    # climate filters
    climate_predicates = climateSim.construct_filters(processed_statement.climate_terms())
    logging.info(f"Climate: {climate_predicates}")
    nearby_cities = []
    for loc in location_coordinates:
        nearby_cities.extend(get_cities_with_temperature(
            loc[0], loc[1], search_distances['climate'], climate_predicates
        ))
    nearby_cities = list(set(nearby_cities))
    logging.info(f"Found {len(nearby_cities)} cities nearby: {[x for _, _, x in nearby_cities]}")

    # geofeatures ranking
    nouns = processed_statement.nouns()
    geofeatures_codes = geoSim.construct_filters(nouns)
    logging.info(f"Looking for geofeatures: {geofeatures_codes}")

    # activities ranking
    activities_codes = activitySim.construct_filters(nouns)
    logging.info(f"Looking for activities: {activities_codes}")

    results = []
    logging.info("Calculating scores...")
    results = score_cities_parallelly(nearby_cities, geofeatures_codes, activities_codes, search_distances)

    final_ranking = sorted(results, key=lambda x: -x['score'])
    logging.info(f"Final ranking: {[city['name'] for city in final_ranking]}")
    logging.info(f"Final ranking length: {len(final_ranking)}")

    return final_ranking
