from concurrent.futures import ThreadPoolExecutor
from travelrec.sparql import (
    get_geofeatures,
    get_activities,
)
from itertools import repeat

def score_city(city, params):
    city_latitude, city_longitude, city_name = city
    geofeatures_codes, activities_codes, search_distances = params
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
    print(f"\t{city_name} with {ranking_points} points")
    return(city_name, ranking_points)

def score_cities_parallelly(cities, geofeatures_codes, activities_codes, search_distances):
    threads = len(cities)
    with ThreadPoolExecutor(threads) as ex:
        res = ex.map(score_city, cities, repeat( (geofeatures_codes, activities_codes, search_distances) ))
    return list(res)
