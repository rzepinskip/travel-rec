from concurrent.futures import ThreadPoolExecutor
from travelrec.sparql import (
    get_geofeatures,
    get_activities,
)

def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

class Scoring:
    def __init__(self, cities, geofeatures_codes, activities_codes, search_distances):
        self.cities = cities
        self.geofeatures_codes = geofeatures_codes
        self.activities_codes = activities_codes
        self.search_distances = search_distances

    def score_city(self, city):
        city_latitude, city_longitude, city_name = city
        geofeatures_count = 0
        if len(self.geofeatures_codes) > 0:
            geo_results = get_geofeatures(
                city_latitude, city_longitude, self.search_distances['geofeatures'], self.geofeatures_codes
            )
            geofeatures_count = len(geo_results["results"]["bindings"])

        activities_count = 0
        if len(self.activities_codes) > 0:
            activity_results = get_activities(
                city_latitude, city_longitude, self.search_distances['activities'], self.activities_codes
            )
            activities_count = len(activity_results["results"]["bindings"])

        ranking_points = 2 * geofeatures_count + activities_count
        print(f"\t{city_name} with {ranking_points} points")
        return(city_name, ranking_points)

    def score_cities_parallelly(self):
        threads = len(self.cities)
        results = multithreading(self.score_city, self.cities, threads)
        return results
