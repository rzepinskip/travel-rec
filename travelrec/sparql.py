import geocoder
from SPARQLWrapper import SPARQLWrapper, JSON
import geopy.distance


def get_location(name):
    loc = geocoder.geonames(name, key="travelrec")

    if loc.code == 'PCLI':
        return 'COUNTRY_CODE', loc.country_code
    else:
        return 'COORD', loc.lat, loc.lng


def get_predicates_declarations(predicates):
    predicates_str = [f"dbp:{predicate.property_name} {predicate.field_name}" for predicate in predicates]
    return "; ".join(predicates_str)

def get_predicates_filters(predicates):
    return "(" + " || ".join([predicate.predicate for predicate in predicates]) + ")"

def get_cities_with_temperature_near_point(latitude, longitude, max_distance, predicates, limit = 35):
    return get_cities_with_temperature(f'gdb-geo:nearby({latitude} {longitude} "{max_distance}km")', predicates)

def get_cities_with_temperature_in_country(country_code, predicates, limit = 35):
    return get_cities_with_temperature(f'gn:countryCode "{country_code}"', predicates)

def get_cities_with_temperature(search_query, predicates, limit = 35):
    sparql = SPARQLWrapper("http://factforge.net/repositories/ff-news")
    query = f"""# Populated places with specified temperature
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX geo-pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX gdb-geo: <http://www.ontotext.com/owlim/geo#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rank: <http://www.ontotext.com/owlim/RDFRank#>
    PREFIX gn: <http://www.geonames.org/ontology#>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?object ?lat ?long
    WHERE {{
    ?object {search_query};
        gn:featureClass  gn:P;
        rank:hasRDFRank3 ?rrank;
            geo-pos:lat ?lat;
            geo-pos:long ?long;
            {get_predicates_declarations(predicates)} .
        FILTER({get_predicates_filters(predicates)} 
            && datatype(?lat) = xsd:float && datatype(?long) = xsd:float
            && STRSTARTS(STR(?object), "http://dbpedia.org/resource")
            )
    }}
    ORDER BY DESC(?rrank)
    LIMIT {limit}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    entities = results["results"]["bindings"]
    cities = []
    for entity in entities:
        entity_lat = entity["lat"]["value"]
        entity_long = entity["long"]["value"]
        entity_name = entity["object"]["value"].split("/")[-1].replace('_', ' ')

        append_city = True

        existing_cities = [c for c in cities if c[2] == entity_name]
        if len(existing_cities) > 0:
            new_city_pt = (entity_lat, entity_long)
            for existing_city in existing_cities:
                existing_city_pt = (existing_city[0], existing_city[1])
                if geopy.distance.distance(new_city_pt, existing_city_pt).km < 10:
                    append_city = False

        if append_city:
            cities.append(
                (
                    entity_lat,
                    entity_long,
                    entity_name,
                )
            )
    return cities


def get_geofeatures(latitude, longitude, max_distance, geo_features, limit=500):
    sparql = SPARQLWrapper("http://factforge.net/repositories/ff-news")
    prefixed_geo_features = [f"gn:{x}" for x in geo_features]
    query = f"""
    PREFIX geo-pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX gdb-geo: <http://www.ontotext.com/owlim/geo#>
    PREFIX rank: <http://www.ontotext.com/owlim/RDFRank#>
    PREFIX gn: <http://www.geonames.org/ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>

    SELECT DISTINCT ?object ?name ?lat ?long ?distance_km
    WHERE {{
        {{
            SELECT ?object ?name ?lat ?long ?distance_km
            WHERE {{
                ?object gdb-geo:nearby({latitude} {longitude} "{max_distance}km");
                        gn:featureCode ?featureCode;
                        geo-pos:lat ?lat;
                        geo-pos:long ?long;
                        dbp:name ?name;
                BIND (omgeo:distance({latitude}, {longitude}, ?lat, ?long) AS ?distance_km).
                FILTER(?featureCode IN ({", ".join(prefixed_geo_features)})) 
            }}
        }}
        FILTER(datatype(?lat) = xsd:float && datatype(?long) = xsd:float)
    }}
    ORDER BY ?distance_km
    LIMIT {limit}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def get_activities(latitude, longitude, max_distance, actitivies, limit=500):
    sparql = SPARQLWrapper(
        "http://geoknow-server.imis.athena-innovation.gr:11480/sparql"
    )
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
            BIND (bif:st_distance(bif:st_point({longitude}, {latitude}), ?fWKT ) AS ?distance_km) .
            FILTER (?distance_km < {max_distance} && ?fCategory_Val IN ({", ".join(actitivies_quoted)}))
        }}
    ORDER BY ?distance_km
    LIMIT {limit}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results
