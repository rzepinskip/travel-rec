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

search_distances = {
    'climate': 300,
    'geofeatures': 150,
    'activities': 75
}

def recommendations_pipeline(query, nlp, verbose=False):
    climateSim = ClimateSimilarity()
    geoSim = GeoFeaturesSimilarity()
    activitySim = ActvitySimilarity()

    if verbose:
        print(f"Query: {query}")
    processed_statement = ProcessedStatement(query)
    # location specification
    location_entities = processed_statement.location_entities()
    if verbose:
        print(f"Locations: {location_entities}")

    loc = location_entities[0].text
    latitude, longitude = get_location(loc)
    if verbose:
        print(f"Coordinates: {loc} - ({latitude}, {longitude})")

    # climate filters
    climate_predicates = climateSim.construct_filters(processed_statement.climate_terms())
    climate_predicate = climate_predicates[0]
    if verbose:
        print(f"Climate: {climate_predicate}")
    nearby_cities = get_cities_with_temperature(
        latitude, longitude, search_distances['climate'], climate_predicate
    )
    if verbose:
        print(f"Found {len(nearby_cities)} cities nearby: {[x for _, _, x in nearby_cities]}")

    # geofeatures ranking
    nouns = processed_statement.nouns()
    geofeatures_codes = geoSim.construct_filters(nouns)
    if verbose:
        print(f"Looking for geofeatures: {geofeatures_codes}")

    # activities ranking
    activities_codes = activitySim.construct_filters(nouns)
    if verbose:
        print(f"Looking for activities: {activities_codes}")

    results = []
    if verbose:
        print("Calculating scores...")
    for city_latitude, city_longitude, city_name in nearby_cities:
        geofeatures_count = 0
        if len(geofeatures_codes) > 0:
            geo_results = get_geofeatures(
                city_latitude, city_longitude, search_distances['geofeatures'], geofeatures_codes
            )
            geofeatures_count = len(geo_results["results"]["bindings"])

        activities_count = 0
        if len(activities_codes) > 0:
            activity_results = get_activities(
                city_latitude, city_longitude, search_distances['activities'], activities_codes
            )
            activities_count = len(activity_results["results"]["bindings"])

        ranking_points = 2 * geofeatures_count + activities_count
        if verbose:
            print(f"\t{city_name} with {ranking_points} points")
        results.append((city_name, ranking_points))

    final_ranking = [x for x, _ in sorted(results, key=lambda x: -x[1])]
    if verbose:
        print(f"Final ranking: {final_ranking}")

    return final_ranking
