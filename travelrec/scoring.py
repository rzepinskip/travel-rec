from concurrent.futures import ThreadPoolExecutor
from travelrec.sparql import (
    get_geofeatures,
    get_activities,
)
from itertools import repeat
import logging

def score_city(city, params):
    city_latitude, city_longitude, city_name = city
    geofeatures_codes, activities_codes, search_distances = params
    geofeatures_count = 0
    if len(geofeatures_codes) > 0:
        geo_results = get_geofeatures(
            city_latitude, city_longitude, search_distances['geofeatures'], geofeatures_codes
        )
        geofeatures_res = geo_results["results"]["bindings"]
        geofeatures_count = len(geofeatures_res)
        geofeatures_places = [{
            'name': gf['name']['value'],
            'coordinates': f"POINT({gf['long']['value']} {gf['lat']['value']})",
            'distance': gf['distance_km']['value']
            } for gf in geofeatures_res] 

    activities_count = 0
    if len(activities_codes) > 0:
        activity_results = get_activities(
            city_latitude, city_longitude, search_distances['activities'], activities_codes
        )
        activiteis_res = activity_results["results"]["bindings"]
        activities_count = len(activiteis_res)
        activities_places = [{
            'name': act['name']['value'],
            'coordinates': act['fWKT']['value'],
            'distance': act['distance_km']['value']
            } for act in activiteis_res]

    ranking_points = 2 * geofeatures_count + activities_count
    logging.info(f"\t{city_name} with {ranking_points} points")
    return { 'name': city_name, 'score': ranking_points, 'geofeatures_places': geofeatures_places, 'activities_places': activities_places }

def score_cities_parallelly(cities, geofeatures_codes, activities_codes, search_distances):
    threads = len(cities)
    with ThreadPoolExecutor(threads) as ex:
        res = ex.map(score_city, cities, repeat( (geofeatures_codes, activities_codes, search_distances) ))
    return list(res)
