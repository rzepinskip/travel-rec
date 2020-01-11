from multiprocessing.dummy import Pool as ThreadPool
from travelrec.sparql import (
    get_geofeatures,
    get_activities,
)

class Scoring:
    def __init__(self, cities, geofeatures_codes, activities_codes):
        self.cities = cities
        self.geofeatures_codes = geofeatures_codes
        self.activities_codes = activities_codes

    def score_city(self, city):
        city_latitude, city_longitude, city_name = city
        geofeatures_count = 0
        if len(self.geofeatures_codes) > 0:
            geo_results = get_geofeatures(
                city_latitude, city_longitude, 350, self.geofeatures_codes
            )
            geofeatures_count = len(geo_results["results"]["bindings"])

        activities_count = 0
        if len(self.activities_codes) > 0:
            activity_results = get_activities(
                city_latitude, city_longitude, 4300, self.activities_codes
            )
            activities_count = len(activity_results["results"]["bindings"])

        ranking_points = 2 * geofeatures_count + activities_count
        print(f"\t{city_name} with {ranking_points} points")
        return(city_name, ranking_points)

    def score_cities_parallelly(self, threads=2):
        pool = ThreadPool(threads)
        results = pool.map(self.score_city, self.cities)
        pool.close()
        pool.join()
        return results
