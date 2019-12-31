import geocoder
from SPARQLWrapper import SPARQLWrapper, JSON

# "near X" - get long, lat of X
# "in X" - use bounding box https://geocoder.readthedocs.io/providers/GeoNames.html#details-inc-timezone-bbox

g = geocoder.geonames("London", key="travelrec")

g.lat
g.lng


def get_cities_with_temperature():
    """# Populated places with specified temperature
    
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX geo-pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX gdb-geo: <http://www.ontotext.com/owlim/geo#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rank: <http://www.ontotext.com/owlim/RDFRank#>
    PREFIX gn: <http://www.geonames.org/ontology#>
    PREFIX dbp: <http://dbpedia.org/property/>

    SELECT DISTINCT ?object ?featureCode ?rrank ?yearHighC
    WHERE {
    { SELECT * { dbr:London geo-pos:lat ?london_lat ; geo-pos:long ?lond_nlong . } LIMIT 1 }
    ?object gdb-geo:nearby(?london_lat ?lond_nlong "25mi");
        gn:featureCode ?featureCode;
        gn:featureClass  gn:P;
        rank:hasRDFRank3 ?rrank;
            geo-pos:lat ?lat;
            geo-pos:lat ?long;
            dbp:yearHighC ?yearHighC .
    } 
    ORDER BY DESC(?rrank)
    """


def get_geofeatures(latitude, longitude):
    sparql = SPARQLWrapper("http://factforge.net/repositories/ff-news")
    geo_features = ["gn:T.BCHS"]
    query = f"""
    PREFIX geo-pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX gdb-geo: <http://www.ontotext.com/owlim/geo#>
    PREFIX rank: <http://www.ontotext.com/owlim/RDFRank#>
    PREFIX gn: <http://www.geonames.org/ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?object ?featureCode ?rrank ?lat ?long ?dist
    WHERE {{
    ?object gdb-geo:nearby({latitude} {longitude} "550km");
        gn:featureCode ?featureCode;
        rank:hasRDFRank3 ?rrank;
            geo-pos:lat ?lat_r;
            geo-pos:lat ?long_r . 
        BIND (xsd:float(?lat_r) as ?lat)
        BIND (xsd:float(?long_r) as ?long)
        BIND (gdb-geo:distance(?lat, ?long, {latitude}, {longitude}) AS ?dist)
        FILTER(?featureCode IN ({", ".join(geo_features)}))
    }}
    ORDER BY DESC(?rrank)
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def get_activities(latitude, longitude):
    sparql = SPARQLWrapper(
        "http://geoknow-server.imis.athena-innovation.gr:11480/sparql"
    )
    actitivies = ["FOOTBALL"]
    actitivies_quoted = [f'"{x}"' for x in actitivies]
    query = f"""
    PREFIX slipo: <http://slipo.eu/def#> 
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    SELECT ?name ?fWKT ?distance_km
    WHERE {{ 
        ?uri slipo:name ?fName . 
            ?fName slipo:nameValue ?name . 
            ?uri slipo:category ?fCategory .
        ?fCategory slipo:value ?fCategory_Val .
        ?uri geo:hasGeometry ?fGeometry .
            ?fGeometry geo:asWKT ?fWKT .
            BIND (bif:st_distance(bif:st_point({latitude}, {longitude}), ?fWKT ) AS ?distance_km) .
            FILTER (?distance_km < 4700 && ?fCategory_Val IN ({", ".join(actitivies_quoted)}))
        }}
    ORDER BY ?distance_km		
                
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


geo_results = get_geofeatures(g.lat, g.lng)
geofeatures_count = len(geo_results["results"]["bindings"])

activity_results = get_geofeatures(g.lat, g.lng)
activities_count = len(activity_results["results"]["bindings"])

