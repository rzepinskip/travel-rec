import logging
from travelrec.similarity import (
    ClimateSimilarity,
    GeoFeaturesSimilarity,
    ActvitySimilarity,
)
from travelrec.sparql import (
    get_location,
    get_cities_with_temperature_near_point,
    get_cities_with_temperature_in_country,
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
    message = "Sorry, we didn't find any location in your query."

    def __str__(self):
        return NoLocationsFoundError.message

class MoreThanOneLocationFoundError(Exception):
    """Raised when more than one location were found based on provided query"""
    message = "Please provide only one location in your query."
    
    def __str__(self):
        return MoreThanOneLocationFoundError.message

class NoNearbyCitiesWithTemperatureFoundError(Exception):
    """Raised when no cities with temperature were found"""
    message = "Sorry, we didn't find any places around."
    
    def __str__(self):
        return NoNearbyCitiesWithTemperatureFoundError.message

class NoNearbyCitiesFoundError(Exception):
    """Raised when getting cities with specified climate results with empty list"""
    message = "Sorry, we didn't find any places meeting the climate conditions."
    
    def __str__(self):
        return NoNearbyCitiesFoundError.message

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
    if len(location_entities) > 1:
        raise MoreThanOneLocationFoundError

    geocoded_locations = [get_location(loc.text) for loc in location_entities]
    logging.info("Coordinates:")
    for loc, geocoded_loc in zip(location_entities, geocoded_locations):
        logging.info(f"\t{loc} - ({geocoded_loc})")

    # climate filters
    climate_predicates = climateSim.construct_filters(processed_statement.climate_terms())
    logging.info(f"Climate: {climate_predicates}")
    nearby_cities = []
    for geocoded_loc in geocoded_locations:
        if geocoded_loc[0] == 'COORD':
            nearby_cities.extend(get_cities_with_temperature_near_point(
                geocoded_loc[1], geocoded_loc[2], search_distances['climate'], climate_predicates
            ))
        elif geocoded_loc[0] == 'COUNTRY_CODE':
            nearby_cities.extend(get_cities_with_temperature_in_country(
                geocoded_loc[1], climate_predicates
            ))
    nearby_cities = list(set(nearby_cities))
    logging.info(f"Found {len(nearby_cities)} cities nearby: {[x for _, _, x in nearby_cities]}")

    if len(nearby_cities) == 0:
        if len(climate_predicates) == 0:
            raise NoNearbyCitiesWithTemperatureFoundError
        else:
            raise NoNearbyCitiesFoundError

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
